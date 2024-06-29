# coding=utf-8
# This script has been installed as a service
# 	/etc/systemd/system/alo_vo.service
# You can enable/disable it using
#	sudo systemctl enable alo_vo

import os
import xdg, xdg.BaseDirectory
import time
import RPi.GPIO as GPIO
import time
import pygame
#from getch import getch

# Constante para resolver oscillações no input dum pin
DEBOUNCE = 200

# Nome da Pasta de sons
CUR_DIR = xdg.BaseDirectory.xdg_data_home + "/" + "alo_vo"
SAVED_DIR = CUR_DIR + "/" + "salvos"

# Constantes dos pins
PIN_LED_VERMELHO1  = 16
PIN_LED_VERMELHO2  = 38
PIN_LED_VERMELHO3  = 11
PIN_BOTAO_GRAVAR   = 18
PIN_LED_BRANCO1    = 33
PIN_LED_BRANCO2    = 35
PIN_LED_BRANCO3    = 12
PIN_BOTAO_PLAYBACK = 29

# Tempo de piscar
PISCAR = 0.5


# ----------- Funções de ajuda

def createFolders():
	if not os.path.exists(CUR_DIR):
		os.mkdir(CUR_DIR)
	if not os.path.exists(SAVED_DIR):
		os.mkdir(SAVED_DIR)

def getFilesInFolder(path):
	return [f for f in os.listdir(path) if os.path.isfile(path + "/" + f)]

def hasSounds():
	return len(getFilesInFolder(CUR_DIR)) >= 1

def getCreationTime(item):
	return os.stat(CUR_DIR + "/" + item).st_ctime

def getQuestion():
	dir = getFilesInFolder(CUR_DIR)
	if hasSounds():
		sortedDir = sorted(dir, key=getCreationTime, reverse=True)
		question = pygame.mixer.Sound(CUR_DIR + "/" + sortedDir[0])
		question.play()
		time.sleep(question.get_length())
		if len(dir) > 1:
			for i in range(1, len(dir)):
				os.rename(CUR_DIR + "/" + sortedDir[i], SAVED_DIR + "/" + sortedDir[i])

# Inicializar o RPi
def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(PIN_LED_VERMELHO1, GPIO.OUT)
	GPIO.setup(PIN_LED_VERMELHO2, GPIO.OUT)
	GPIO.setup(PIN_LED_VERMELHO3, GPIO.OUT)
	GPIO.setup(PIN_BOTAO_GRAVAR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(PIN_LED_BRANCO1, GPIO.OUT)
	GPIO.setup(PIN_LED_BRANCO2, GPIO.OUT)
	GPIO.setup(PIN_LED_BRANCO3, GPIO.OUT)
	GPIO.setup(PIN_BOTAO_PLAYBACK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	createFolders()
	while (True):
		try:
			pygame.mixer.init(frequency=44100)
			break
		except:
			print("Failed to start audio device. Trying again in 5 seconds")
			time.sleep(5)

# Mudar o estado do LED
def led(pin, enable):
	GPIO.output(pin, enable)

# Função para testar botao
debouncer_lastvalue = {}
def botao(pin):
	global debouncer_lastvalue

	# Como a chave do dicionario não pode ser um numero, vamos converter-lo em string
	chave = str(pin)

	# Lê a eletrecidade no pin
	value = GPIO.input(pin)

	# Se este pin não estiver guardado, vamos ter que cria-lo primeiro
	if (not chave in debouncer_lastvalue):
		debouncer_lastvalue[chave] = 0

	# Se o pin estiver a 1, aumenta o valor do debouncer uma vez, se não, faz reset a zero
	if (value == 1):
		debouncer_lastvalue[chave] += 1
	else:
		debouncer_lastvalue[chave] = 0

	# Se o debouncer for igual ou maior ao valor de DEBOUNCE, retornar true
	if (debouncer_lastvalue[chave] >= DEBOUNCE):
		return True
	else:
		return False



# ----------- Loop do programa
def terminar():
	pygame.mixer.quit()
	exit()

# Loop que corre para sempre
def loop():

	botao_gravar_antigo = False
	botao_playback_antigo = False
	gravando = False
	led_branca_ligada = hasSounds()
	led_vermelho_ligado = False
	led_vermelho_tempo = 0

	while (True):
		botao_playback_agora = botao(PIN_BOTAO_PLAYBACK)
		botao_gravar_agora = botao(PIN_BOTAO_GRAVAR)

		# Fechar o programa quando carregarmos em ESC
		#if ord(getch()) == 27:
		#	terminar()

		# Piscar LED Vermelho quando o botão gravar está pressionado
		if (botao_gravar_agora and not botao_gravar_antigo):
			if (gravando == False):
				gravando = True
			else:
				gravando = False
		if (gravando == True):
			if(led_vermelho_tempo < time.perf_counter()):
				led_vermelho_tempo = time.perf_counter() + PISCAR
				if (led_vermelho_ligado == True):
					led_vermelho_ligado = False
				else:
					led_vermelho_ligado = True
		else:
			led_vermelho_ligado = False
		led(PIN_LED_VERMELHO1, led_vermelho_ligado)
		led(PIN_LED_VERMELHO2, led_vermelho_ligado)
		led(PIN_LED_VERMELHO3, led_vermelho_ligado)

		# Desligar LED branca quando todos os sons já foram ouvidos
		if(botao_playback_agora and not botao_playback_antigo):
			getQuestion()
			led_branca_ligada = False
		led(PIN_LED_BRANCO1, led_branca_ligada)
		led(PIN_LED_BRANCO2, led_branca_ligada)
		led(PIN_LED_BRANCO3, led_branca_ligada)
		botao_playback_antigo = botao_playback_agora
		botao_gravar_antigo = botao_gravar_agora

# ----------- Correr programa

# O Python corre estas funções
setup()
loop()
