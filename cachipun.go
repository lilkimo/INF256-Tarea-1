package main

import (
	"fmt"
	"math/rand"
	"net"
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

			case "ISAVAILABLE?":
				if isAvailable() {
					data = "OK"
				} else {
					data = "NO"
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
