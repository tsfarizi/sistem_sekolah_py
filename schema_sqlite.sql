-- Schema SQLITE — generated from SQLAlchemy ORM

CREATE TABLE kelas (
	id INTEGER NOT NULL, 
	nama VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nama)
);

CREATE TABLE mata_pelajaran (
	id INTEGER NOT NULL, 
	nama VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nama)
);

CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(50) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	role VARCHAR(20) NOT NULL, 
	nama VARCHAR(100) NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);

CREATE TABLE guru (
	id VARCHAR(20) NOT NULL, 
	nama VARCHAR(100) NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE siswa (
	nis VARCHAR(20) NOT NULL, 
	nama VARCHAR(100) NOT NULL, 
	kelas_id INTEGER NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (nis), 
	FOREIGN KEY(kelas_id) REFERENCES kelas (id) ON DELETE CASCADE, 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE guru_mengajar (
	id INTEGER NOT NULL, 
	guru_id VARCHAR(20) NOT NULL, 
	kelas_id INTEGER NOT NULL, 
	mata_pelajaran_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_guru_kelas_matapelajaran UNIQUE (guru_id, kelas_id, mata_pelajaran_id), 
	FOREIGN KEY(guru_id) REFERENCES guru (id) ON DELETE CASCADE, 
	FOREIGN KEY(kelas_id) REFERENCES kelas (id) ON DELETE CASCADE, 
	FOREIGN KEY(mata_pelajaran_id) REFERENCES mata_pelajaran (id) ON DELETE CASCADE
);

CREATE TABLE nilai (
	id INTEGER NOT NULL, 
	nis VARCHAR(20) NOT NULL, 
	guru_mengajar_id INTEGER NOT NULL, 
	tugas FLOAT NOT NULL, 
	uts FLOAT NOT NULL, 
	uas FLOAT NOT NULL, 
	nilai_akhir FLOAT NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(nis) REFERENCES siswa (nis) ON DELETE CASCADE, 
	FOREIGN KEY(guru_mengajar_id) REFERENCES guru_mengajar (id) ON DELETE CASCADE
);
