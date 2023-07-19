{
  fromYaml,
  projectPath,
  outputs,
  ...
}: let
  composition = let
    reverseList = xs: let l = builtins.length xs; in builtins.genList (n: builtins.elemAt xs (l - n - 1)) l;
    apply = x: f: f x;
  in
    # composition of functions
    functions: val: builtins.foldl' apply val (reverseList functions);
  sizes_conf = fromYaml (
    builtins.readFile (
      projectPath "/common/compute/arch/sizes/data.yaml"
    )
  );
  compute_resources = size: {
    vcpus = sizes_conf."${size}".cpu;
    inherit (sizes_conf."${size}") memory;
    inherit (sizes_conf."${size}") queue;
  };
  scheduled_job = {
    name,
    attempts,
    timeout,
    size,
    command,
  }:
    {
      inherit attempts command;
      attemptDurationSeconds = timeout;
      definition = "prod_observes";
      environment = [
        "CACHIX_AUTH_TOKEN"
      ];
      setup = [outputs."/secretsForAwsFromGitlab/prodObserves"];
      tags = {
        "Name" = name;
        "management:area" = "cost";
        "management:product" = "observes";
        "management:type" = "product";
      };
    }
    // compute_resources size;

  with_universe_token = job: job // {environment = job.environment ++ ["UNIVERSE_API_TOKEN"];};
  parrallel_job = parallel: let
    parallel_conf =
      if parallel >= 2
      then {inherit parallel;}
      else {};
  in
    job: job // parallel_conf;

  clone_job = {
    name,
    attempts,
    timeout,
    command,
  }:
    scheduled_job {
      inherit name attempts timeout command;
      size = "observes_clone";
    }
    // {
      queue = "observes_clone";
    };
in {
  computeOnAwsBatch = {
    observesCodeEtlUpload = composition [with_universe_token scheduled_job] {
      name = "code_upload";
      size = "observes_small";
      attempts = 3;
      timeout = 8 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/code/upload"];
    };

    observesDynamoSchema = scheduled_job {
      name = "dynamo_etl_determine_schema";
      size = "observes_large";
      attempts = 3;
      timeout = 1 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/jobs/determine-schema"];
    };

    observesDynamoSchemaTestData = scheduled_job {
      name = "dynamo_etl_determine_schema_test_data";
      size = "observes_small";
      attempts = 3;
      timeout = 3 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/jobs/determine-schema-test-data"];
    };

    observesDynamoParallelPhase1 = parrallel_job 240 (scheduled_job {
      name = "dynamo_etl_parallel_1";
      size = "observes_small";
      attempts = 5;
      timeout = 24 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/jobs/parallel-phase-1"];
    });

    observesDynamoRetryPhase1 = scheduled_job {
      name = "dynamo_etl_retry_1";
      size = "observes_small";
      attempts = 5;
      timeout = 24 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/jobs/parallel-phase-1"];
    };

    observesDynamoParallelPhase3 = parrallel_job 240 (scheduled_job {
      name = "dynamo_etl_parallel_3";
      size = "observes_small";
      attempts = 1;
      timeout = 24 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/jobs/parallel-phase-3"];
    });

    observesDynamoRetryPhase3 = scheduled_job {
      name = "dynamo_etl_retry_3";
      size = "observes_small";
      attempts = 5;
      timeout = 24 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/jobs/parallel-phase-3"];
    };
    observesRecalcHash = scheduled_job {
      name = "dynamo_etl_recalc_hash";
      size = "observes_small";
      attempts = 1;
      timeout = 24 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/code/recalc"];
    };
  };
}
