package main

import (
	"fmt"
	"math/rand"
	"net"
	"strings"
	"time"
)

func isAvailable() bool {
	rand.Seed(time.Now().UnixNano())
	min := 1
	max := 10
	result := rand.Intn(max-min+1) + min
	if result == 1 {
		return false
	}
	return true
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
		fmt.Print("-> ", string(buffer), "\n")

		var data string
		switch strings.TrimSpace(string(buffer[0:n])) {
		case "STOP":
			fmt.Println("Exiting UDP server!")
			return
		case "ISAVAILABLE?":
			if isAvailable() {
				data = "OK"
			} else {
				data = "NO"
			}
		}

		_, err = connection.WriteToUDP([]byte(data), addr)
		if err != nil {
			fmt.Println(err)
			return
		}
	}
}
