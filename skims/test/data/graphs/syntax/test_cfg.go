package main

import (
	"errors"
	"fmt"
	"log"
	"net/http"
	"github.com/julienschmidt/httprouter"
)

type Class struct{}

func (this *Class) CapturePanic(h httprouter.Handle) {
	var err error
	r := recover()
	if r != nil {
		switch t := r.(type) {
		case string:
			err = errors.New(t)
		case error:
			err = t
		default:
			err = errors.New("Unknown error")
		}
		log.Println(err.Error())
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func (this *Class) DetectSQLMap(h httprouter.Handle) httprouter.Handle {
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
		userAgent := r.Header.Get("User-Agent")
		sqlmapDetected, _ := regexp.MatchString("sqlmap*", userAgent)
		if sqlmapDetected {
			w.WriteHeader(http.StatusForbidden)
			w.Write([]byte("Forbidden"))
			log.Printf("sqlmap detect ")
			return
		} else {
			h(w, r, ps)
		}
	}
}

func (this *Class) AuthCheck(h httprouter.Handle) httprouter.Handle {
	var sess = session.New()
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
		if !sess.IsLoggedIn(r) {
			redirect := "/login"
			http.Redirect(w, r, redirect, http.StatusSeeOther)
			return
		}

		h(w, r, ps)
	}
}

type Profile struct {
	Uid         int
	Name        string
	City        string
	PhoneNumber string
}

func (p *Profile) UnsafeQueryGetData(uid string) error {

	/* comment */
	DB, err = database.Connect()

	getProfileSql := fmt.Sprintf(`SELECT p.user_id, p.full_name, p.city, p.phone_number
								FROM Profile as p,Users as u
								where p.user_id = u.id
								and u.id=%s`, uid) // inline comment
	rows, err := DB.Query(getProfileSql)
	if err != nil {
		return err
	}
	defer rows.Close()
	var profile = Profile{}
	for rows.Next() {
		err = rows.Scan(&p.Uid, &p.Name, &p.City, &p.PhoneNumber)
		if err != nil {
			log.Printf("Row scan error: %s", err.Error())
			return err
		}
	}
	return nil
}

func (p *Profile) SafeQueryGetData(uid string) error {

	DB, err = database.Connect()

	const (
		getProfileSql = `SELECT p.user_id, p.full_name, p.city, p.phone_number
		FROM Profile as p,Users as u
		where p.user_id = u.id
		and u.id=?`
	)

	stmt, err := DB.Prepare(getProfileSql)
	if err != nil {
		return err
	}

	defer stmt.Close()
	err = stmt.QueryRow(uid).Scan(&p.Uid, &p.Name, &p.City, &p.PhoneNumber)
	if err != nil {
		return err
	}
	return nil
}

type Self struct{}

func (self *Self) IsLoggedIn(r *http.Request) bool {
	s, err := store.Get(r, "govwa")
	if err != nil {
		log.Println(err.Error())
	}
	if auth, ok := s.Values["govwa_session"].(bool); !ok || !auth {
		return false
	}
	return true
}

func (self *Self) SetSession(w http.ResponseWriter, r *http.Request, data map[string]string) {
	session, err := store.Get(r, "govwa")

	if err != nil {
		log.Println(err.Error())
	}

	session.Options = &sessions.Options{
		Path:     "/",
		MaxAge:   3600,
		HttpOnly: false,
	}

	session.Values["govwa_session"] = true

	if data != nil {
		for key, value := range data {
			session.Values[key] = value
		}
	}

	err = session.Save(r, w)
	if err != nil {
		log.Println(err.Error())
	}
}


func CheckLevel(r *http.Request) bool {
	level := GetCookie(r, "Level")
	if level == "" || level == "low" {
		return false
	} else if level == "high" {
		return true
	} else {
		return false
	}
}

func Connect() (*sql.DB, error) {
	config := config.LoadConfig()

	var dsn string
	var db *sql.DB

	dsn = fmt.Sprintf("%s:%s@tcp(%s:%s)/", config.User, config.Password, config.Sqlhost, config.Sqlport)
	db, err := sql.Open("mysql", dsn)

	if err != nil {
		return nil, err
	}
	_, err = db.Exec("CREATE DATABASE IF NOT EXISTS " + config.Dbname)

	if err != nil {
		return nil, err
	} else {
		dsn = fmt.Sprintf("%s:%s@tcp(%s:%s)/%s", config.User, config.Password, config.Sqlhost, config.Sqlport, config.Dbname)
		db, err = sql.Open("mysql", dsn)

		if err != nil {
			return nil, err

		}
	}
	return db, nil
}

func DeleteCookie(w http.ResponseWriter, cookies []string){
	for _,name := range cookies{
		cookie := &http.Cookie{
			Name:     name,
			Value:    "",
			Expires: time.Unix(0, 0),
		}
		http.SetCookie(w, cookie)
	}
}

func GetOSVersion() string {
	switch os := runtime.GOOS; os{
	case "darwin":
		return "OS X"
	case "linux":
		return "Linux"
	default:
		fmt.Printf("%s.", os)
	}
	return ""
}

func PrintVars() {
	var i, j int = 1, 2
	k := 3
	c, python, java := true, false, "no!"
	fmt.Println(i, j, k, c, python, java)
}

func ForLoops() {
	var i, sum int
	for i = 0; i<10; i++ {
		fmt.Println("For with assignment")
	}

	for j := 0; j < 10; j++ {
		sum += j
		fmt.Println("For with var declaration")
	}

	sum = 1
	for ; sum < 1000; {
		sum += sum
		fmt.Println("For with condition only")
	}

	sum = 1
	for sum < 1000 {
		sum += sum
		fmt.Println("For as while")
	}

	for {
		fmt.Println("Continuous For")
	}
}
