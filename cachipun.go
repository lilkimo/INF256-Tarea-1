package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"time"
)

func generateRandomPort() string {
	rand.Seed(time.Now().UnixNano())
	min := 49154
	max := 65535
	result := rand.Intn(max-min+1) + min
	return strconv.Itoa(result)
}

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

func generarJugada() string {
	rand.Seed(time.Now().UnixNano())
	min := 1
	max := 3
	result := rand.Intn(max-min+1) + min
	if result == 1 {
		return "ROCK"
	} else if result == 2 {
		return "PAPER"
	} else {
		return "SCISSORS"
	}
}

func main() {
	fmt.Println("Iniciando servidor cachipun.")
	PORT := ":50004"
	BUFFER := 1024

	udpAddr, err := net.ResolveUDPAddr("udp4", PORT)
	if err != nil {
		fmt.Println(err)
		return
	}
	connection, err := net.ListenUDP("udp4", udpAddr)
	if err != nil {
		fmt.Println(err)
		return
	}

	defer connection.Close()
	buffer := make([]byte, BUFFER)

	var response string
	for {
		n, addr, err := connection.ReadFromUDP(buffer)
		response = string(buffer[0:n])
		fmt.Printf("[IN ] %s\n", response)
		
		var data string
		switch response {
			case "STOP":
				data = "OK"
				_, err = connection.WriteToUDP([]byte(data), addr)
				if err != nil {
					fmt.Println(err)
					return
				}
				fmt.Printf("[OUT] %s\nApagando el servidor...\n", data)
				return

			case "REQUESTGAME":
				if isAvailable() {
					randomPort := generateRandomPort()
					udpAddrRandom, err := net.ResolveUDPAddr("udp4", ":" + randomPort)
					if err != nil {
						fmt.Println(err)
						return
					}
					connectionRandom, err := net.ListenUDP("udp4", udpAddrRandom)
					if err != nil {
						fmt.Println(err)
						return
					}
					defer connectionRandom.Close()
					data = "OK," + randomPort
					fmt.Println(data)
				} else {
					data = "NO,"
				}

			case "GETSHAPE":
				data = generarJugada()
		}
		_, err = connection.WriteToUDP([]byte(data), addr)
		if err != nil {
			fmt.Println(err)
			return
		}
		fmt.Printf("[OUT] %s\n", data)
	}
}
