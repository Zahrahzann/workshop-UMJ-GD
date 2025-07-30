import pygame # Fungsi untuk perintah untuk mengimpor library Pygame, yaitu library Python yang dirancang khusus untuk membuat game dan aplikasi multimedia.
from pygame.locals import * #Baris ini mengimpor semua konstanta (variabel yang sudah ditentukan) dan fungsi yang tersedia di modul pygame.locals.
import random #Library random adalah pustaka bawaan Python yang digunakan untuk menghasilkan nilai acak.

#inisialisasi modul 
pygame.init() 

#frame per second 
clock = pygame.time.Clock() # Untuk membatasi jumlah frame per detik (FPS) agar permainan berjalan mulus.
fps = 60  #mengatur seberapa cepat game akan berjalan. Ini berarti setiap detik, komputer akan memproses dan menggambar 60 frame untuk game.

 #pengaturan layar 
screen_width = 864 # menentukan ukuran layar permainan.
screen_height = 936 #menentukan tinggi ukuran layar permainan 
screen = pygame.display.set_mode((screen_width, screen_height)) #digunakan untuk membuat layar utama.
pygame.display.set_caption('Flappy Bird')  #mengatur judul jendela.

#definisi  font
font = pygame.font.SysFont('Bauhaus 93', 60) #mendefinisikan jenis dan ukuran font untuk teks.

#definisi warna 
white = (255, 255, 255)  #berfungsi untuk mengatur warna 


#definisi variabel permainan 
ground_scroll = 0 # Variabel ini menyimpan posisi horizontal dari ground (tanah) dalam game
scroll_speed = 4   # Menentukan kecepatan scroll atau pergeseran dari tanah dan pipa dalam game.
flying = False    # Variabel ini berfungsi sebagai indikator apakah burung sedang terbang atau tidak.
game_over = False  # Variabel ini berfungsi sebagai penanda apakah permainan telah berakhir atau belum.
pipe_gap = 150    #Variabel ini menentukan jarak vertikal (gap) antara pipa atas dan bawah.
pipe_frequency = 1500 #Mengatur jarak antara pipa (vertikal) dan waktu untuk menghasilkan pipa baru (dalam milidetik)
last_pipe = pygame.time.get_ticks() - pipe_frequency  #fungsi untuk mendapatkan waktu saat ini sejak game dimulai.
score = 0   #Variabel ini menyimpan skor permainan.
pass_pipe = False  #Variabel ini digunakan untuk mendeteksi apakah burung sudah melewati pipa tertentu atau belum.


#muat gambar 

#gambar latar
bg = pygame.image.load('latar.png')  #fungsi latar belakang dari Pygame yang digunakan untuk memuat file gambar dari folder proyek, 

#gambar ground / alas 
ground_img = pygame.image.load('ground.png')  #Fungsi ini memuat file gambar alas atau ground kedalam variabel ground.png

#gambar tombol atau button 
button_img = pygame.image.load('restart.png') #Fungsi ini memuat file gambar restart.png ke dalam variabel button_img


#fungsi menampilkan layar ke text
def draw_text(text, font, text_col, x, y):  #Fungsi ini digunakan untuk menampilkan teks pada layar game
	img = font.render(text, True, text_col)  #Mengubah teks menjadi gambar dengan menggunakan font dan warna yang diberikan.
	screen.blit(img, (x, y))   #Menampilkan gambar teks (img) di layar pada koordinat (x, y).

#mengatur ulang posisi burung, skor dan pipa 
def reset_game():   #Fungsi ini digunakan untuk me-reset kondisi permainan setelah pemain kalah atau memulai ulang.
	pipe_group.empty()  #Menghapus semua pipa yang ada di layar
	flappy.rect.x = 100  #Mengatur posisi horizontal burung (Flappy Bird) kembali ke posisi awal (koordinat x = 100).
	flappy.rect.y = int(screen_height / 2)  #Mengatur posisi vertikal burung di tengah layar (koordinat y = tengah dari layar).
	score = 0   #menyetel score kembali ke nol saat permainan di-reset.
	return score   #Mengembalikan nilai skor ke nol.

#Kelas Burung atau sprite animasi pada burung 

class Bird(pygame.sprite.Sprite): #berfungsi untuk mendefinisikan karakter burung
	
	def __init__(self, x, y):  #bagian konstruktor dalam pemrograman Python, yang digunakan untuk menginisialisasi objek yang dibuat dari kelas
		pygame.sprite.Sprite.__init__(self)  #Inisialisasi sprite dari kelas Sprite
		self.images = []  #Sebuah daftar yang menyimpan gambar-gambar burung untuk animasi.
		self.index = 0    #Menunjukkan gambar mana yang saat ini digunakan dari daftar self.images untuk animasi burung.
		self.counter = 0   #Penghitung waktu untuk mengatur kapan animasi burung berubah ke frame berikutnya.		
		for num in range (1, 4):  #fungsi Perulangan dilakukan 3 kali, dengan num bernilai 1, 2, dan 3 secara bertahap.
			
			#gambar burung di simpan dan di perbarui setiap frame 
			img = pygame.image.load(f"bird{num}.png")  #fungsi bawaan dari library Pygame yang digunakan untuk memuat (load) file gambar ke dalam program.
			
			self.images.append(img)   #Menambahkan gambar ke dalam list
		self.image = self.images[self.index]  #Mengatur gambar awal burung
		self.rect = self.image.get_rect()  #Mendapatkan dimensi dari gambar
		self.rect.center = [x, y]  #bagian penting untuk mengatur posisi sprite (seperti burung, tabrakan objek, dll.
		self.vel = 0  #mengatur kecepatan dari burung saat game di mulai
		self.clicked = False  #bagian dari inisialisasi atribut objek burung bertujuan untuk melacak apakah pemain telah melakukan klik pada mouse 

	def update(self):  #berfungsi untuk mengelola berbagai aspek perilaku burung selama permainan berlangsung. 

		if flying == True:  #kondisi yang memeriksa apakah permainan sedang dalam keadaan "terbang" (burung dapat bergerak). 

			#gravitasi game physics 
			self.vel += 0.5  #variabel yang menyimpan kecepatan vertikal burung, yang digunakan untuk mensimulasikan gravitasi
			if self.vel > 8:  #berfungsi untuk membatasi kecepatan vertikal burung saat jatuh ke bawah, yang disebabkan oleh efek gravitasi. 
				self.vel = 8   #berfungsi untuk menetapkan batas kecepatan vertikal maksimal burung saat jatuh ke bawah akibat efek gravitasi.
			if self.rect.bottom < 768:  #berfungsi untuk memastikan bahwa burung tidak bergerak ke bawah melewati batas bawah layar, atau lebih tepatnya, untuk mencegah burung keluar dari layar ketika jatuh karena gravitasi.
				self.rect.y += int(self.vel) #berfungsi untuk memperbarui posisi vertikal burung berdasarkan kecepatan vertikal (gravitasi) yang disimulasikan dalam game.

		if game_over == False: #berfungsi untuk mengecek apakah permainan masih berlanjut atau sudah berakhir
			
			#lompatan game physics 
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:  #berfungsi untuk mendeteksi apakah pemain menekan tombol kiri mouse (klik pertama), dan memastikan bahwa burung belum melompat pada klik sebelumnya. 
				self.clicked = True  #berfungsi untuk menandai bahwa burung telah melompat setelah pemain mengklik mouse
				self.vel = -10   #berfungsi  mengatur kecepatan lompatan burung ketika pemain mengklik mouse.
			if pygame.mouse.get_pressed()[0] == 0: #berfungsi untuk memeriksa kondisi ketika tombol kiri mouse tidak ditekan dalam permainan Flappy Bird.
				self.clicked = False  #berfungsi untuk menyimpan status apakah tombol mouse sudah ditekan atau belum.

			#menangani animasi 
			flap_cooldown = 5  #berfungsi untuk mengontrol kecepatan animasi lompatan burung (flap) dan untuk mencegah burung melakukan lompatan terlalu cepat berulang-ulang.
			self.counter += 1  #berfungsi untuk menghitung jumlah frame yang telah berlalu sejak penghitungan dimulai, dan dapat digunakan untuk tujuan seperti mengatur animasi atau logika waktu tertentu dalam permainan
			
			#animasi burung di kontrol dengan menghitung waktu ( counter ) dan mengganti gambar secara bergantian 
			if self.counter > flap_cooldown:  #berfungsi untuk mengatur seberapa sering animasi burung berubah
				self.counter = 0 #berfungsi untuk mengatur ulang penghitung ke nilai 0. Ini dilakukan setiap kali gambar burung diperbarui untuk memastikan bahwa penghitung dimulai kembali dari 0
				self.index += 1 #berfungsi untuk memperbarui indeks untuk memilih gambar burung yang sedang ditampilkan dalam animasi.
				if self.index >= len(self.images):  #berfungsi untuk memeriksa indeks yang bertujuan memastikan bahwa indeks yang digunakan untuk mengakses gambar burung tidak melebihi batas yang ada dalam daftar gambar burung.
					self.index = 0  #berfungsi untuk menginisialisasi yang merupakan variabel yang menyimpan indeks gambar burung yang sedang ditampilkan.
				self.image = self.images[self.index]   #berfungsi untuk memperbarui gambar burung yang ditampilkan berdasarkan nilai indeks akan menyimpan gambar burung yang sesuai dengan indeks yang ditentukan


			#rotasi memutar burung 
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)  #berfungsi untuk memutar (rotate) gambar burung berdasarkan kecepatan vertikal
		else:  #digunakan dalam struktur pengambilan keputusan (conditional statement) pada Python. 
			
			#arah burung ke tanah 
			self.image = pygame.transform.rotate(self.images[self.index], -90)  #berfungsi dalam struktur pemrograman game Flappy Bird untuk memutar gambar burung (sprite burung) sebesar -90 derajat. 

#Kelas Animasi Pada Pipa atau Sprite Pipa 

class Pipe(pygame.sprite.Sprite): #berfungsi untuk deklarasi kelas objek pipa dalam game Flappy Bird. 

	def __init__(self, x, y, position):   #berfungsi untuk metode konstruktor dalam Python. Dalam konteks game Flappy Bird
		pygame.sprite.Sprite.__init__(self)  #berfungsi untuk  memanggil konstruktor dari kelas induk bagian dari sistem hierarki kelas di Pygame
		self.image = pygame.image.load("pipe.png")  #berfungsi untuk memuat gambar (sprite) pipa ke dalam permainan. 
		self.rect = self.image.get_rect()  #bagian penting dalam pemrograman Python untuk game Flappy Bird.
		#posisi variabel menentukan apakah pipa datang dari bawah atau atas 
		#posisi 1 dari atas , posisi -1 dari bawah 
		if position == 1:  #berfungsi untuk menentukan posisi objek di layar pada kondisi percabangan yang memeriksa nilai dari variabel
			self.image = pygame.transform.flip(self.image, False, True)  #berfungsi untuk membalikkan (flip) gambar objek secara vertikal.
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)] #berfungsi untuk menentukan posisi dari objek sprite (dalam hal ini, pipa) di layar, dengan memperhatikan jarak vertikal antar pipa
		elif position == -1:  #berfungsi untuk memproses pipa bawah
			self.rect.topleft = [x, y + int(pipe_gap / 2)] #berfungsi mengatur posisi sprite pipa di layar


	def update(self):  #berfungsi untuk memperbarui kondisi atau status objek dalam game setiap frame
		self.rect.x -= scroll_speed  #berfungsi untuk memperbarui posisi objek (misalnya pipa atau latar belakang) dalam permainan dengan cara menggeser objek ke kiri pada setiap frame
		if self.rect.right < 0: #berfungsi untuk memeriksa apakah objek (seperti pipa) telah keluar dari layar di sisi kanan. 
			self.kill()   #berfungsi untuk pengelolaan objek-objek yang ada dalam permainan, khususnya objek yang tidak lagi dibutuhkan 

#kelas button 

class Button():  #berfungsi untuk mengelola elemen antarmuka pengguna (UI) yang interaktif, seperti tombol untuk memulai permainan, 
	def __init__(self, x, y, image):  #merupakan bagian dari konstruktor untuk kelas yang menginisialisasi objek baru, seperti objek untuk bird atau pipe
		self.image = image  #berfungsi untuk mengatur gambar atau sprite yang akan digunakan untuk objek (seperti burung atau pipa) dalam game.
		self.rect = self.image.get_rect()  # bagian penting yang berhubungan dengan pengaturan posisi dan ukuran objek (seperti burung atau pipa) dalam game. 
		self.rect.topleft = (x, y) #berfungsi untuk mengatur objek , objek tersebut termasuk ( burung dan tombol)

	def draw(self):  #berfungsi untuk menggambar tombol pada layar dan memeriksa apakah tombol tersebut telah diklik oleh pemain
		action = False

		#posisi mouse 
		pos = pygame.mouse.get_pos() #berfungsi Mengambil posisi kursor mouse saat ini di layar.

		#periksa kondisi mouse dan klik 
		if self.rect.collidepoint(pos): #berfungsi Mengecek apakah posisi mouse berada di dalam area tombol.
			if pygame.mouse.get_pressed()[0] == 1: #berfungsi Mengecek apakah tombol kiri mouse (button 0) diklik.
				action = True

		#tombol gambar 
		screen.blit(self.image, (self.rect.x, self.rect.y))  #berfungsi untuk menggambar (atau "merender") objek grafis pada layar. 

		return action #berfungsi Jika tombol diklik, Action akan bernilai True yang dapat digunakan untuk mengaktifkan aksi selanjutnya (misalnya memulai ulang permainan).



pipe_group = pygame.sprite.Group() #berfungsi untuk Membuat grup objek pipa yang akan bergerak di layar.

#menambahkan animasi burung ke dalam grup 
bird_group = pygame.sprite.Group() #berfungsi untuk Membuat grup untuk objek burung yang dikendalikan oleh pemain.

flappy = Bird(100, int(screen_height / 2)) #berfungsi untuk konteks pengembangan game Flappy Bird menggunakan Python dan Pygame adalah cara untuk membuat objek Bird yang mewakili burung dalam permainan.

bird_group.add(flappy)  #berfungsi untuk konteks pembuatan game Flappy Bird menggunakan Python dan Pygame bertujuan untuk menambahkan objek 

#buat contoh tombol ulang 
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)  #berfungsi untuk membuat objek Button yang merupakan instance kelas button


run = True
while run:

	clock.tick(fps) #berfungsi untuk mengatur kecepatan frame per detik (FPS) dan memastikan bahwa game berjalan dengan kecepatan yang konstan. 

	#menggambar latar belakang 
	screen.blit(bg, (0,0)) #berfungsi untuk menggambar atau menampilkan suatu gambar  ke layar.

	pipe_group.draw(screen) #berfungsi untuk menggambar semua objek pipa yang tergabung dalam pipe group ke layar utama 
	bird_group.draw(screen)  #berfungsi untuk menggambar semua sprite burung yang berada di dalam grup
	bird_group.update()  #berfungsi untuk memperbarui (update) semua sprite burung yang berada di dalam grup 

	#gambar latar atau alas di ulang setiap frame 
	screen.blit(ground_img, (ground_scroll, 768)) #berfungsi untuk menggambar ground (tanah/lantai) pada layar game Flappy Bird dengan menggunakan fungsi


#perhitungan score 
	if len(pipe_group) > 0:  #berfungsi untuk memeriksa apakah terdapat pipa dalam grup 
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and pass_pipe == False:
			pass_pipe = True
		if pass_pipe == True: #Variabel ini biasanya digunakan untuk menentukan apakah burung telah melewati pipa tertentu dalam game 
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score += 1 #berfungsi untuk menyimpan jumlah poin atau skor dalam game. 
				pass_pipe = False
				
		#skor di tampilkan di tengah layar 
	draw_text(str(score), font, white, int(screen_width / 2), 20) #berfungsi untuk Menampilkan skor pemain pada layar dalam bentuk teks.


	#deteksi tabrakan 
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: #berfungsi untuk mengecek tabrakan antara burung dan pipa 
		game_over = True  #berfungsi untuk menandai bahwa permainan telah berakhir 
	
	#logika game over atau permainan berakhir 
	if flappy.rect.bottom >= 768: #berfungsi untuk memeriksa apakah bagian bawah burung (Flappy Bird) telah mencapai atau melewati batas bawah layar permainan
		game_over = True  #berfungsi untuk mengubah variabel permainan sebagai indikator menandakan bahwa permainan telah selesai.
		flying = False  #Variabel ini digunakan untuk menentukan status apakah burung sedang dalam keadaan terbang (flying) atau tidak.


	if flying == True and game_over == False: #berfungsi untuk memeriksa apakah burung sedang terbang atau Memeriksa apakah permainan belum berakhir.
		
		#membuat pipa baru 
		time_now = pygame.time.get_ticks()  #berfungsi untuk mendapatkan jumlah waktu yang telah berlalu sejak program dimulai dalam satuan milidetik
		if time_now - last_pipe > pipe_frequency:  #berfungsi untuk memeriksa apakah waktu yang telah berlalu sejak pembuatan pipa terakhir
			pipe_height = random.randint(-100, 100) #berfungsi untuk menghasilkan nilai acak untuk ketinggian pipa (atau posisi pipa) dalam permainan
			btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1) #berfungsi untuk membuat objek pipa bawah pada game 
			top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)  #Variabel ini digunakan untuk menyimpan objek Pipe yang mewakili pipa bagian atas dalam game Flappy Bird.
			pipe_group.add(btm_pipe)  #berfungsi untuk menyimpan dan mengelola beberapa objek pipa secara bersamaan dalam satu grup.
			pipe_group.add(top_pipe)  #sebuah grup atau koleksi objek Pipe digunakan untuk menyimpan dan mengelola beberapa objek pipa secara bersamaan dalam satu grup
			last_pipe = time_now  #Variabel ini digunakan untuk menyimpan waktu terakhir kali pipa baru dibuat atau ditambahkan ke layar.
		
		#gerakan animasi pada pipa 
		pipe_group.update()  #sebuah grup atau koleksi objek pipa (termasuk pipa atas dan bawah) yang biasanya dikelola. 

		#membuat latar belakang 
		ground_scroll -= scroll_speed #fungsi untuk menggerakkan latar belakang (ground) ke kiri, menciptakan efek pergerakan yang memberikan kesan bahwa karakter (flappy bird) sedang terbang melewati dunia dalam game
		if abs(ground_scroll) > 35: #berfungsi untuk memicu pergerakan ulang dari tanah agar game tidak terlihat berhenti atau terhenti dalam aspek visual. 
			ground_scroll = 0  #berfungsi untuk menyimpan posisi horizontal dari tanah dalam permainan.
	

	#memulai ulang setelah game over 
	if game_over == True: #berfungsi untuk memeriksa apakah permainan telah berakhir atau belum.
		if button.draw(): #bagian dari logika yang berhubungan dengan interaksi pengguna dalam permainan, khususnya untuk menampilkan dan menangani aksi yang berkaitan dengan tombol atau button
			game_over = False  #variabel yang digunakan untuk menyimpan status permainan, apakah permainan sudah berakhir atau belum
			score = reset_game()  #berfungsi untuk mengatur ulang permainan setelah permainan selesai (misalnya setelah game over).

		#loop utama game 
	for event in pygame.event.get(): #berfungsi menangani event atau kejadian yang terjadi dalam game, seperti input dari pemain (misalnya, menekan tombol keyboard atau klik mouse) atau peristiwa lainnya yang berkaitan dengan permainan
		if event.type == pygame.QUIT: #berfungsi untuk memeriksa apakah event yang terjadi ketika pemain mencoba menutup jendela game
			run = False  #berfungsi untuk  menghentikan atau mengontrol status utama game, seperti menentukan apakah game sedang berjalan atau tidak.
		
		#interaksi Pengguna 
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:  #berfungsi untuk mendeteksi apakah pengguna mengklik mouse pada saat kondisi tertentu terpenuhi, dan digunakan untuk mengontrol apakah burung dalam game Flappy Bird akan mulai terbang atau tidak,
			flying = True

		#memperbarui tampilan setiap frame 
	pygame.display.update()  #berfungsi untuk memperbarui seluruh layar atau area tertentu dari jendela permainan

#mengakhiri suatu permainan atau game 
pygame.quit() #berfungsi untuk menutup dan mengakhiri semua permainan.