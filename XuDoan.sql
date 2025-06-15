-- Tạo CSDL XuDoan
CREATE DATABASE XuDoan;

-- Xóa CSDL XuDoan
DROP DATABASE XuDoan;

-- Sử dụng CSDL XuDoan
USE XuDoan;


-- Tạo các bảng trong CSDL XuDoan
CREATE TABLE `ThieuNhi` (
  `idThieuNhi` varchar(12) PRIMARY KEY NOT NULL,
  `tenThanh` tinytext,
  `hoTen` tinytext NOT NULL,
  `ngaySinh` date NOT NULL,
  `giaoXu` tinytext NOT NULL,
  `ngayRuaToi` date,
  `ngayRuocLe` date,
  `ngayThemSuc` date,
  `diaChi` tinytext NOT NULL,
  `matKhau` char(40),
  `ghiChu` tinytext
);

CREATE TABLE `PhuHuynh` (
  `idPhuHuynh` varchar(13) PRIMARY KEY NOT NULL,
  `tenThanh` tinytext,
  `hoTen` tinytext NOT NULL,
  `soDienThoai` tinytext NOT NULL,
  `matKhau` char(40)
);

CREATE TABLE `ThieuNhi_PhuHuynh` (
  `idThieuNhi` varchar(12) NOT NULL,
  `idPhuHuynh` varchar(13) NOT NULL,
  `vaiTro` enum('Cha','Mẹ','Người giám hộ') NOT NULL,
  PRIMARY KEY (`idThieuNhi`, `idPhuHuynh`)
);

CREATE TABLE `PhanDoan` (
  `idPhanDoan` varchar(10) PRIMARY KEY NOT NULL,
  `tenPhanDoan` tinytext NOT NULL,
  `namHoc` tinytext NOT NULL,
  `nganh` enum('Chiên Con','Ấu Nhi','Thiếu Nhi','Nghĩa Sĩ','Hiệp Sĩ') NOT NULL
);

CREATE TABLE `PhanDoan_ThieuNhi` (
  `idPhanDoan` varchar(10) NOT NULL,
  `idThieuNhi` varchar(12) NOT NULL,
  `hocKy` bit(2) NOT NULL,
  `diemKiemTra1` decimal(10,2),
  `diemKiemTra2` decimal(10,2),
  `diemKiemTra3` decimal(10,2),
  `diemThi` decimal(10,2),
  `diemTrungBinh` decimal(10,2),
  `hocLuc` enum('Xuất sắc','Giỏi','Khá','Trung bình','Yếu'),
  `hanhKiem` enum('Đạt','Không đạt'),
  PRIMARY KEY (`idThieuNhi`, `idPhanDoan`, `hocKy`)
);

CREATE TABLE `DiemDanh` (
  `idThieuNhi` varchar(12) NOT NULL,
  `idPhanDoan` varchar(10) NOT NULL,
  `ngayDiemDanh` date NOT NULL,
  `thoiGianDiemDanh` timestamp,
  `coMatThanhLe` bool,
  `diTreThanhLe` bool,
  `coMatGiaoLy` bool,
  `vangPhep` bool,
  PRIMARY KEY (`idThieuNhi`, `idPhanDoan`, `ngayDiemDanh`)
);

CREATE TABLE `NhanSu` (
  `idNhanSu` varchar(10) PRIMARY KEY NOT NULL,
  `tenThanh` tinytext NOT NULL,
  `hoTen` tinytext NOT NULL,
  `chucDanh` enum('Linh mục','Tu sĩ','Nữ tu'),
  `hoiDong` tinytext,
  `ngaySinh` date,
  `giaoXu` tinytext,
  `soDienThoai` tinytext,
  `email` tinytext,
  `diaChi` tinytext,
  `dangHoatDong` bool NOT NULL,
  `matKhau` char(40)
);

CREATE TABLE `PhanDoan_NhanSu` (
  `idPhanDoan` varchar(10) NOT NULL,
  `idNhanSu` varchar(10) NOT NULL,
  `vaiTro` enum('Phân Đoàn Trưởng','Phân Đoàn Phó','Huấn Giáo','Huynh Trưởng','Dự Trưởng') NOT NULL,
  PRIMARY KEY (`idPhanDoan`, `idNhanSu`)
);

CREATE TABLE `PhanDoan_TroTa` (
  `idPhanDoan` varchar(10) NOT NULL,
  `idTroTa` varchar(13) NOT NULL
);

ALTER TABLE `ThieuNhi_PhuHuynh` ADD FOREIGN KEY (`idThieuNhi`) REFERENCES `ThieuNhi` (`idThieuNhi`);

ALTER TABLE `ThieuNhi_PhuHuynh` ADD FOREIGN KEY (`idPhuHuynh`) REFERENCES `PhuHuynh` (`idPhuHuynh`);

ALTER TABLE `PhanDoan_ThieuNhi` ADD FOREIGN KEY (`idPhanDoan`) REFERENCES `PhanDoan` (`idPhanDoan`);

ALTER TABLE `PhanDoan_ThieuNhi` ADD FOREIGN KEY (`idThieuNhi`) REFERENCES `ThieuNhi` (`idThieuNhi`);

ALTER TABLE `DiemDanh` ADD FOREIGN KEY (`idThieuNhi`) REFERENCES `ThieuNhi` (`idThieuNhi`);

ALTER TABLE `DiemDanh` ADD FOREIGN KEY (`idPhanDoan`) REFERENCES `PhanDoan` (`idPhanDoan`);

ALTER TABLE `PhanDoan_NhanSu` ADD FOREIGN KEY (`idPhanDoan`) REFERENCES `PhanDoan` (`idPhanDoan`);

ALTER TABLE `PhanDoan_NhanSu` ADD FOREIGN KEY (`idNhanSu`) REFERENCES `NhanSu` (`idNhanSu`);

ALTER TABLE `PhanDoan_TroTa` ADD FOREIGN KEY (`idPhanDoan`) REFERENCES `PhanDoan` (`idPhanDoan`);

ALTER TABLE `PhanDoan_TroTa` ADD FOREIGN KEY (`idTroTa`) REFERENCES `PhuHuynh` (`idPhuHuynh`);


-- Thêm các bản ghi vào bảng NhanSu
INSERT INTO XuDoan.NhanSu
(idNhanSu, tenThanh, hoTen, chucDanh, hoiDong, ngaySinh, giaoXu, soDienThoai, email, diaChi, dangHoatDong, matKhau)
VALUES('NSVP050403', 'Martinô', 'Võ Huỳnh Thanh Phương', null, '', '2003-04-05', 'Tân Hòa', '0869367710', 'phuong.vht.0504@gmail.com', '', 1, '$2b$12$JHD9amf2Ze6aQQCxEGZmku8d3lbT5KzOxS6FACGIwjYfbg2WAEqpK');

INSERT INTO XuDoan.NhanSu
(idNhanSu, tenThanh, hoTen, chucDanh, hoiDong, ngaySinh, giaoXu, soDienThoai, email, diaChi, dangHoatDong, matKhau)
VALUES('NSVP190201', 'Giuse', 'Võ Văn Phong', null, '', '2001-02-19', 'Thủ Đức', '0986557412', 'phong.vv.1902@gmail.com', '', 0, '$2b$12$JHD9amf2Ze6aQQCxEGZmku8d3lbT5KzOxS6FACGIwjYfbg2WAEqpK');


-- Thêm các bản ghi vào bảng PhanDoan
INSERT INTO XuDoan.PhanDoan
(idPhanDoan, tenPhanDoan, namHoc, nganh)
VALUES('AN1-024025', 'Ấu Nhi 1', '2024-2025', 'Ấu Nhi');


-- Thêm các bản ghi vào bảng PhanDoan_NhanSu
INSERT INTO XuDoan.PhanDoan_NhanSu
(idPhanDoan, idNhanSu, vaiTro)
VALUES('AN1-024025', 'NSVP050403', 'Huynh Trưởng');


-- Thêm các bản ghi vào bảng ThieuNhi
INSERT INTO XuDoan.ThieuNhi
(idThieuNhi, tenThanh, hoTen, ngaySinh, giaoXu, ngayRuaToi, ngayRuocLe, ngayThemSuc, diaChi, matKhau, ghiChu)
VALUES('TNNA05042017', 'Anna', 'Nguyễn Thị An', '2017-05-04', 'Hà Nội (Đồng Nai)', '2017-06-04', null, null, 'Chưa biết', '$2b$12$JHD9amf2Ze6aQQCxEGZmku8d3lbT5KzOxS6FACGIwjYfbg2WAEqpK', '');

INSERT INTO XuDoan.ThieuNhi
(idThieuNhi, tenThanh, hoTen, ngaySinh, giaoXu, ngayRuaToi, ngayRuocLe, ngayThemSuc, diaChi, matKhau, ghiChu)
VALUES('TNTD06012017', 'Maria', 'Trần Bảo Dương', '2017-01-06', 'Đa Minh', null, null, null, '19 Lê Quý Đôn, phường 11, quận Phú Nhuận', '$2b$12$JHD9amf2Ze6aQQCxEGZmku8d3lbT5KzOxS6FACGIwjYfbg2WAEqpK', '');

INSERT INTO XuDoan.ThieuNhi
(idThieuNhi, tenThanh, hoTen, ngaySinh, giaoXu, ngayRuaToi, ngayRuocLe, ngayThemSuc, diaChi, matKhau, ghiChu)
VALUES('TNNT30092017', 'Gioan Phaolô II', 'Nguyễn Trường Thịnh', '2017-09-30', 'Tân Sa Châu', '2017-10-08', null, null, '2 Nguyễn Thanh Tuyền, phường 2, quận Tân Bình', '$2b$12$JHD9amf2Ze6aQQCxEGZmku8d3lbT5KzOxS6FACGIwjYfbg2WAEqpK', '');


-- Thêm các bản ghi vào bảng PhuHuynh và bảng ThieuNhi_PhuHuynh
INSERT INTO XuDoan.PhuHuynh
(idPhuHuynh, tenThanh, hoTen, soDienThoai, matKhau)
VALUES('PHT0123456789', 'Giuse', 'Nguyễn Thanh', '0123456789', '$2b$12$JHD9amf2Ze6aQQCxEGZmku8d3lbT5KzOxS6FACGIwjYfbg2WAEqpK');

INSERT INTO XuDoan.ThieuNhi_PhuHuynh
(idThieuNhi, idPhuHuynh, vaiTro)
VALUES('TNNA05042017', 'PHT0123456789', 'Cha');

INSERT INTO XuDoan.PhuHuynh
(idPhuHuynh, tenThanh, hoTen, soDienThoai, matKhau)
VALUES('PHT0909176772', 'Maria', 'Lê Trâm', '0909176772', '$2b$12$JHD9amf2Ze6aQQCxEGZmku8d3lbT5KzOxS6FACGIwjYfbg2WAEqpK');

INSERT INTO XuDoan.ThieuNhi_PhuHuynh
(idThieuNhi, idPhuHuynh, vaiTro)
VALUES('TNNA05042017', 'PHT0909176772', 'Mẹ');

INSERT INTO XuDoan.PhuHuynh
(idPhuHuynh, tenThanh, hoTen, soDienThoai, matKhau)
VALUES('PHT0987654321', 'Micae', 'Trần Thọ', '0987654321', '$2b$12$JHD9amf2Ze6aQQCxEGZmku8d3lbT5KzOxS6FACGIwjYfbg2WAEqpK');

INSERT INTO XuDoan.ThieuNhi_PhuHuynh
(idThieuNhi, idPhuHuynh, vaiTro)
VALUES('TNTD06012017', 'PHT0987654321', 'Cha');

INSERT INTO XuDoan.PhuHuynh
(idPhuHuynh, tenThanh, hoTen, soDienThoai, matKhau)
VALUES('PHT0909196807', 'Maria Mađalêna', 'Mai Trang', '0909196807', '$2b$12$JHD9amf2Ze6aQQCxEGZmku8d3lbT5KzOxS6FACGIwjYfbg2WAEqpK');

INSERT INTO XuDoan.ThieuNhi_PhuHuynh
(idThieuNhi, idPhuHuynh, vaiTro)
VALUES('TNTD06012017', 'PHT0909196807', 'Mẹ');

INSERT INTO XuDoan.PhuHuynh
(idPhuHuynh, tenThanh, hoTen, soDienThoai, matKhau)
VALUES('PHT0912345678', 'Đaminh', 'Nguyễn Thế', '0912345678', '$2b$12$JHD9amf2Ze6aQQCxEGZmku8d3lbT5KzOxS6FACGIwjYfbg2WAEqpK');

INSERT INTO XuDoan.ThieuNhi_PhuHuynh
(idThieuNhi, idPhuHuynh, vaiTro)
VALUES('TNNT30092017', 'PHT0912345678', 'Cha');

INSERT INTO XuDoan.PhuHuynh
(idPhuHuynh, tenThanh, hoTen, soDienThoai, matKhau)
VALUES('PHT0931460461', 'Maria', 'La Hoàng Thuý', '0931460461', '$2b$12$JHD9amf2Ze6aQQCxEGZmku8d3lbT5KzOxS6FACGIwjYfbg2WAEqpK');

INSERT INTO XuDoan.ThieuNhi_PhuHuynh
(idThieuNhi, idPhuHuynh, vaiTro)
VALUES('TNNT30092017', 'PHT0931460461', 'Mẹ');


-- Thêm các bảng ghi vào bảng PhanDoan_ThieuNhi
INSERT INTO XuDoan.PhanDoan_ThieuNhi
(idPhanDoan, idThieuNhi, hocKy, diemKiemTra1, diemKiemTra2, diemKiemTra3, diemThi, diemTrungBinh, hocLuc, hanhKiem)
VALUES('AN1-024025', 'TNNA05042017', 1, 8.0, 7.0, 9.0, 9.0, 8.4, 'Giỏi', 'Đạt');

INSERT INTO XuDoan.PhanDoan_ThieuNhi
(idPhanDoan, idThieuNhi, hocKy, diemKiemTra1, diemKiemTra2, diemKiemTra3, diemThi, diemTrungBinh, hocLuc, hanhKiem)
VALUES('AN1-024025', 'TNNA05042017', 2, null, null, null, null, null, null, null);

INSERT INTO XuDoan.PhanDoan_ThieuNhi
(idPhanDoan, idThieuNhi, hocKy, diemKiemTra1, diemKiemTra2, diemKiemTra3, diemThi, diemTrungBinh, hocLuc, hanhKiem)
VALUES('AN1-024025', 'TNTD06012017', 1, 10.0, 5.3, 6.5, 8.3, 7.7, 'Khá', 'Đạt');

INSERT INTO XuDoan.PhanDoan_ThieuNhi
(idPhanDoan, idThieuNhi, hocKy, diemKiemTra1, diemKiemTra2, diemKiemTra3, diemThi, diemTrungBinh, hocLuc, hanhKiem)
VALUES('AN1-024025', 'TNTD06012017', 2, 7.5, null, null, null, null, null, null);

INSERT INTO XuDoan.PhanDoan_ThieuNhi
(idPhanDoan, idThieuNhi, hocKy, diemKiemTra1, diemKiemTra2, diemKiemTra3, diemThi, diemTrungBinh, hocLuc, hanhKiem)
VALUES('AN1-024025', 'TNNT30092017', 1, 10.0, 5.0, 7.8, 8.0, 7.8, 'Khá', 'Đạt');

INSERT INTO XuDoan.PhanDoan_ThieuNhi
(idPhanDoan, idThieuNhi, hocKy, diemKiemTra1, diemKiemTra2, diemKiemTra3, diemThi, diemTrungBinh, hocLuc, hanhKiem)
VALUES('AN1-024025', 'TNNT30092017', 2, 5.0, null, null, null, null, null, null);


-- Thêm các bảng ghi vào bảng DiemDanh (idThieuNhi=='TNNA05042017')
INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-09-08', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-09-15', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-09-22', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-09-29', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-10-06', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-10-13', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-10-20', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-10-27', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-11-03', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-11-10', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-11-17', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-11-24', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-12-01', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-12-08', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-12-15', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-12-22', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2024-12-29', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2025-01-05', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2025-01-12', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2025-02-09', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2025-02-16', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2025-02-23', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2025-03-02', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2025-03-09', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2025-03-06', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2025-03-23', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2025-03-30', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNA05042017', 'AN1-024025', '2025-04-06', null, 0, 0, 0, 0);


-- Thêm các bảng ghi vào bảng DiemDanh (idThieuNhi=='TNTD06012017')
INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-09-08', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-09-15', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-09-22', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-09-29', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-10-06', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-10-13', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-10-20', null, null, null, null, null);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-10-27', null, null, null, null, null);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-11-03', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-11-10', null, null, null, null, null);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-11-17', null, null, null, null, null);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-11-24', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-12-01', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-12-08', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-12-15', null, 1, 1, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-12-22', null, 1, 1, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2024-12-29', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2025-01-05', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2025-01-12', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2025-02-09', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2025-02-16', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2025-02-23', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2025-03-02', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2025-03-09', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2025-03-16', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2025-03-23', null, null, null, null, null);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2025-03-30', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNTD06012017', 'AN1-024025', '2025-04-06', null, 1, 0, 1, 0);


-- Thêm các bảng ghi vào bảng DiemDanh (idThieuNhi=='TNNT30092017')
INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-09-08', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-09-15', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-09-22', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-09-29', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-10-06', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-10-13', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-10-20', null, null, null, null, null);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-10-27', null, null, null, null, null);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-11-03', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-11-10', null, null, null, null, null);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-11-17', null, null, null, null, null);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-11-24', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-12-01', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-12-08', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-12-15', null, 1, 1, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-12-22', null, 1, 1, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2024-12-29', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2025-01-05', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2025-01-12', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2025-02-09', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2025-02-16', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2025-02-23', null, 0, 0, 0, 1);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2025-03-02', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2025-03-09', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2025-03-16', null, 0, 0, 0, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2025-03-23', null, null, null, null, null);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2025-03-30', null, 1, 0, 1, 0);

INSERT INTO XuDoan.DiemDanh
(idThieuNhi, idPhanDoan, ngayDiemDanh, thoiGianDiemDanh, coMatThanhLe, diTreThanhLe, coMatGiaoLy, vangPhep)
VALUES('TNNT30092017', 'AN1-024025', '2025-04-06', null, 1, 0, 1, 0);

SHOW GRANTS FOR 'root'@'localhost';

-- Thể hiện bảng NhanSu
SELECT * FROM XuDoan.NhanSu;


-- Thể hiện bảng PhanDoan
SELECT * FROM XuDoan.PhanDoan;


-- Thể hiện bảng ThieuNhi
SELECT * FROM XuDoan.ThieuNhi;


-- Thể hiện bảng PhanDoan
SELECT * FROM XuDoan.PhanDoan;


-- Thể hiện bảng PhanDoan_ThieuNhi
SELECT * FROM XuDoan.PhanDoan_ThieuNhi;


-- Thể hiện bảng PhanDoan_NhanSu
SELECT * FROM XuDoan.PhanDoan_NhanSu;


-- Thể hiện bảng PhanDoan_TroTa
SELECT * FROM XuDoan.PhanDoan_TroTa;

-- Thể hiện bảng PhuHuynh
SELECT * FROM XuDoan.PhuHuynh;

-- Thể hiện bảng DiemDanh
SELECT * FROM XuDoan.DiemDanh;

-- Thể hiện bảng ThieuNhi_PhuHuynh
SELECT * FROM XuDoan.ThieuNhi_PhuHuynh;



