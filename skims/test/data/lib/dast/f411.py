from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "Volumes": [
            {
                "KmsKeyId": "fluidkmskey123/1234",
                "State": "creating",
                "VolumeId": "fluidVolume1",
            },
        ],
        "FileSystems": [
            {
                "FileSystemId": "fluidFS",
                "KmsKeyId": "fluidkey/5678",
            },
            {
                "FileSystemId": "fluidFSX",
                "KmsKeyId": "fluidkey/1279",
            },
        ],
        "Clusters": [
            {
                "ClusterIdentifier": "fluidRedShiftCluster",
                "KmsKeyId": "fluidkey/8888",
            },
        ],
        "Aliases": [
            {
                "AliasName": "alias/aws/ebs",
                "AliasArn": "arn:aws:fluid/aliaskey",
                "TargetKeyId": "1234",
            },
            {
                "AliasName": "alias/aws/elasticfilesystem",
                "TargetKeyId": "5678",
            },
            {
                "AliasName": "alias/aws/fsx",
                "TargetKeyId": "1279",
            },
            {
                "AliasName": "alias/aws/redshift",
                "TargetKeyId": "8888",
            },
        ],
        "SecretList": [
            {
                "KmsKeyId": "fluidkmsKey1",
            }
        ],
        "KeyMetadata": {
            "Arn": "arn:aws:fluidarn/123456",
            "KeyManager": "AWS",
        },
    }
