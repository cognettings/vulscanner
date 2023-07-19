package main

import (
	"golang.org/x/crypto/scrypt"
	"fmt"
)

func unsafeHash(password string,){
	unsafe1 := scrypt.Key([]byte(password), "HARDCODED_SALT", 16384, 8, 1, 32)

	var salt = "HARDCODED_SALT"
	unsafe2 := scrypt.Key([]byte(password), salt, 16384, 8, 1, 32)

	salt2 := []byte("HARDCODED_SALT")
	unsafe3 := scrypt.Key([]byte(password), salt2, 16384, 8, 1, 32)
}

func safeHash(password string, salt []byte){
	random_salt = []byte("salt") + salt
	safe1 := scrypt.Key([]byte(password), salt1, 16384, 8, 1, 32)
	return safe_1
}
