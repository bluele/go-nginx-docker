// main.go
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"net/http"
	"os"
	"strings"

	"github.com/garyburd/redigo/redis"
)

func main() {
	socketPath := "/tmp/app.sock"
	l, err := net.ListenUnix("unix", &net.UnixAddr{socketPath, "unix"})
	if err != nil {
		panic(err)
	}
	defer os.Remove(socketPath)

	http.HandleFunc("/api", func(w http.ResponseWriter, r *http.Request) {
		redi, err := redis.Dial("tcp", "redis:6379")
		if err != nil {
			log.Fatal(err)
		}
		res, err := redi.Do("incr", "counter")
		if err != nil {
			w.WriteHeader(500)
			w.Write([]byte(err.Error()))
			return
		}

		if res, ok := res.(int64); ok {
			w.Write([]byte(fmt.Sprintf("counter: %d", res)))
		} else {
			w.WriteHeader(500)
			w.Write([]byte("unexpected value"))
		}
	})

	log.Println("Start server...")
	log.Fatal(http.Serve(l, http.DefaultServeMux))
}

func listFiles(path string) {
	list, err := ioutil.ReadDir(path)
	if err != nil {
		fmt.Fprintf(os.Stderr, "%v", err)
		os.Exit(1)
	}
	for _, finfo := range list {
		if finfo.IsDir() || -1 == strings.Index(finfo.Name(), ".txt") {
			continue
		}
		fmt.Printf("%q\n", finfo.Name())
	}
}
