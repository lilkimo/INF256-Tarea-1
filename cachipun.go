package main

import (
		"fmt"
		"net"
		"strings"
        "math/rand"
        "time"
)

func disponibilidad(){
        rand.Seed(time.Now().UnixNano())
        min := 1
        max := 10
        //fmt.Println(rand.Intn(max - min + 1) + min)
        return(rand.Intn(max - min + 1) + min)
}

func main() {
        PORT := ":50001"
	    BUFFER := 1024

        s, err := net.ResolveUDPAddr("udp4", PORT)
        if err != nil {
                fmt.Println(err)
                return
        }

        connection, err := net.ListenUDP("udp4", s)
        if err != nil {
                fmt.Println(err)
                return
        }

        defer connection.Close()
        buffer := make([]byte, BUFFER)

        for {
                n, addr, err := connection.ReadFromUDP(buffer)
                fmt.Print("-> ", string(buffer[0:n-1]))

                /*
                rand.Seed(time.Now().UnixNano())
                min := 1
                max := 10
                fmt.Println(rand.Intn(max - min + 1) + min)
                */

                if strings.TrimSpace(string(buffer[0:n])) == "STOP" {
                        fmt.Println("Exiting UDP server!")
                        return
                }

                data := []byte("uwu")
                fmt.Printf("data: %s\n", string(data))
                _, err = connection.WriteToUDP(data, addr)
                if err != nil {
                        fmt.Println(err)
                        return
                }
        }
}