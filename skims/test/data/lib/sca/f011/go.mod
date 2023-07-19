module github.com/javtube/javtube-sdk-go

go 1.19

require (
	github.com/adrg/strutil v0.3.0
	github.com/antchfx/htmlquery v1.2.5
	github.com/araddon/dateparse v0.0.0-20210429162001-6b43995a97de
	github.com/corona10/goimagehash v1.1.0
	github.com/esimov/pigo v1.4.6
	github.com/gin-gonic/gin v1.8.1
	github.com/glebarez/sqlite v1.5.0
	github.com/gocolly/colly/v2 v2.1.1-0.20220706081359-947eeead97b3
	github.com/grafov/m3u8 v0.11.1
	github.com/hashicorp/go-retryablehttp v0.7.1
	github.com/iancoleman/orderedmap v0.2.0
	github.com/jellydator/ttlcache/v3 v3.0.0
	github.com/lib/pq v1.10.7
	github.com/nlnwa/whatwg-url v0.1.2
	github.com/peterbourgon/ff/v3 v3.3.0
	github.com/stretchr/testify v1.8.0
	go.uber.org/atomic v1.9.0
	gogs.io/gogs v0.6.5
	golang.org/x/image v0.0.0-20220902085622-e7cb96979f69
	golang.org/x/text v0.3.8
	gorm.io/datatypes v1.0.7
	gorm.io/driver/postgres v1.4.4
	gorm.io/gorm v1.24.0
)

require (
	github.com/PuerkitoBio/goquery v1.8.0 // indirect
	github.com/andybalholm/cascadia v1.3.1 // indirect
	github.com/antchfx/xmlquery v1.3.12 // indirect
	github.com/antchfx/xpath v1.2.1 // indirect
	github.com/bits-and-blooms/bitset v1.3.3 // indirect
	github.com/davecgh/go-spew v1.1.1 // indirect
	github.com/gin-contrib/sse v0.1.0 // indirect
	github.com/glebarez/go-sqlite v1.19.1 // indirect
	github.com/go-playground/locales v0.14.0 // indirect
	github.com/go-playground/universal-translator v0.18.0 // indirect
	github.com/go-playground/validator/v10 v10.11.1 // indirect
	github.com/go-sql-driver/mysql v1.6.0 // indirect
	github.com/gobwas/glob v0.2.3 // indirect
	github.com/goccy/go-json v0.9.11 // indirect
	github.com/golang/groupcache v0.0.0-20210331224755-41bb18bfe9da // indirect
	github.com/golang/protobuf v1.5.2 // indirect
	github.com/google/uuid v1.3.0 // indirect
	github.com/hashicorp/go-cleanhttp v0.5.2 // indirect
	github.com/jackc/chunkreader/v2 v2.0.1 // indirect
	github.com/jackc/pgconn v1.13.0 // indirect
	github.com/jackc/pgio v1.0.0 // indirect
	github.com/jackc/pgpassfile v1.0.0 // indirect
	github.com/jackc/pgproto3/v2 v2.3.1 // indirect
	github.com/jackc/pgservicefile v0.0.0-20200714003250-2b9c44734f2b // indirect
	github.com/jackc/pgtype v1.12.0 // indirect
	github.com/jackc/pgx/v4 v4.17.2 // indirect
	github.com/jinzhu/inflection v1.0.0 // indirect
	github.com/jinzhu/now v1.1.5 // indirect
	github.com/json-iterator/go v1.1.12 // indirect
	github.com/kennygrant/sanitize v1.2.4 // indirect
	github.com/leodido/go-urn v1.2.1 // indirect
	github.com/mattn/go-isatty v0.0.16 // indirect
	github.com/modern-go/concurrent v0.0.0-20180306012644-bacd9c7ef1dd // indirect
	github.com/modern-go/reflect2 v1.0.2 // indirect
	github.com/nfnt/resize v0.0.0-20180221191011-83c6a9932646 // indirect
	github.com/pelletier/go-toml/v2 v2.0.5 // indirect
	github.com/pmezard/go-difflib v1.0.0 // indirect
	github.com/remyoudompheng/bigfft v0.0.0-20220927061507-ef77025ab5aa // indirect
	github.com/saintfish/chardet v0.0.0-20120816061221-3af4cd4741ca // indirect
	github.com/temoto/robotstxt v1.1.2 // indirect
	github.com/ugorji/go/codec v1.2.7 // indirect
	golang.org/x/crypto v0.0.0-20221012134737-56aed061732a // indirect
	golang.org/x/sync v0.0.0-20220929204114-8fcdb60fdcc0 // indirect
	golang.org/x/sys v0.0.0-20221013171732-95e765b1cc43 // indirect
	golang.org/x/xerrors v0.0.0-20220609144429-65e65417b02f // indirect
	google.golang.org/appengine v1.6.7 // indirect
	google.golang.org/protobuf v1.28.1 // indirect
	gopkg.in/yaml.v2 v2.4.0 // indirect
	gopkg.in/yaml.v3 v3.0.1 // indirect
	gorm.io/driver/mysql v1.4.2 // indirect
	gorm.io/driver/sqlite v1.3.2 // indirect
	modernc.org/libc v1.20.4 // indirect
	modernc.org/mathutil v1.5.0 // indirect
	modernc.org/memory v1.4.0 // indirect
	github.com/imdario/mergo v0.3.12 // indirect
	modernc.org/sqlite v1.19.2 // indirect
)

require	golang.org/x/net v0.0.0-20221014081412-f15817d10f9b

replace github.com/imdario/mergo => github.com/imdario/mergo v0.3.5

replace (
	modernc.org/sqlite v1.19.2 => modernc.org/sqlite v1.19.3
    golang.org/x/net => example.com/fork/net v1.4.5
)
