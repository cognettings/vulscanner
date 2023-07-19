
val key = "gb09ym9ydoolp3w886d0tciczj6ve9kszqd65u7d126040gwy86xqimjpuuc788g"
val db = SQLiteDatabase.openOrCreateDatabase("test.db", key, null) // Noncompliant


val key = "gb09ym9ydoolp3w886d0tciczj6ve9kszqd65u7d126040gwy86xqimjpuuc788g"
val config = RealmConfiguration.Builder().encryptionKey(key.toByteArray()).build()
val realm = Realm.getInstance(config)


val db = SQLiteDatabase.openOrCreateDatabase("test.db", getKey(), null)
Realm

val config = RealmConfiguration.Builder().encryptionKey(getKey()).build()
val realm = Realm.getInstance(config)
