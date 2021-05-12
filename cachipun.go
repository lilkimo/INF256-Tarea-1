package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"time"
)

// Genera un puerto aleatorio para los socket de juego
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
	PORT := ":49153"
	fmt.Println("Iniciando servidor cachipun en el puerto " + PORT)
	BUFFER := 1024

	// Se crea un socket para comunicarse con el servidor intermediario
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

	// Se reciben mensajes del servidor intermediario en donde REQUESTGAME crea un socket para realizar las jugadas del bot y STOP cierra el servidor cachipun
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

				// Si el servidor cachipun se encuentra disponible se procede con la creacion del socket con puerto aleatorio y jugadas aleatorias del bot
				if isAvailable() {
					// Se crea un socket nuevo en un puerto aleatorio
					randomPort := generateRandomPort()
					udpAddrRandom, err := net.ResolveUDPAddr("udp4", ":" + randomPort)
					if err != nil {
						fmt.Println(err)
						return
					}
					gameConnection, err := net.ListenUDP("udp4", udpAddrRandom)
					if err != nil {
						fmt.Println(err)
						return
					}
					bufferGame := make([]byte, BUFFER)
					data := "OK," + randomPort

					// Se envía OK al servidor intermediario con el puerto aleatorio del socket
					_, err = connection.WriteToUDP([]byte(data), addr)
					if err != nil {
						fmt.Println(err)
						return
					}
					fmt.Printf("[OUT] %s\n", data)

					// Se reciben GETSHAPE hasta que se recibe un CLOSE, con lo que avisa al servidor intermediario con OK y se cierra el socket terminando el ciclo
					for {
						nGame, addrGame, err := gameConnection.ReadFromUDP(bufferGame)
						responseGame := string(bufferGame[0:nGame])
						fmt.Printf("[IN ] %s\n", responseGame)

						if responseGame == "GETSHAPE"{
							botShape := generarJugada()
							_, err = gameConnection.WriteToUDP([]byte(botShape), addrGame)
							if err != nil {
								fmt.Println(err)
								return
							}
							fmt.Printf("[OUT] %s\n", botShape)
						} else if responseGame == "CLOSE" {
							_, err = gameConnection.WriteToUDP([]byte("OK"), addrGame)
							if err != nil {
								fmt.Println(err)
								return
							}
							fmt.Printf("Cerrando el puerto %s...\n", randomPort)
							gameConnection.Close()
							break
						}
					}
				
				} else {
					// Si el servidor no se encuentra disponible, le envia 'NO,' (En realidad es coma seguido de un caracter vacío que indica que no se generó puerto) al servidor intermediario
					data = "NO,"
					_, err = connection.WriteToUDP([]byte(data), addr)
					if err != nil {
						fmt.Println(err)
						return
					}
					fmt.Printf("[OUT] %s\n", data)
				}
		}
	}
}
