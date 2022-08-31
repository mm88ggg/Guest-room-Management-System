-- Create a new database called 'HotelManagement'
-- Connect to the 'master' database to run this snippet
USE master
GO
-- Create the new database if it does not exist already
IF NOT EXISTS (
    SELECT [name]
        FROM sys.databases
        WHERE [name] = N'HotelManagement'
)
CREATE DATABASE HotelManagement
GO

USE HotelManagement;

PRINT GETDATE()

-- 预定表
CREATE TABLE [dbo].[Booking] (
    [username] CHAR (20) NOT NULL,
    [roomID]   CHAR (20) NOT NULL,
    [StaffID]  INT       NULL,
    [bookdate] DATETIME  DEFAULT (getdate()) NOT NULL,
    [from]     DATETIME  NOT NULL,
    [to]       DATETIME  NOT NULL,
    [isActive] NCHAR (1) DEFAULT ('是') NOT NULL,
    CONSTRAINT [PK_Booking] PRIMARY KEY CLUSTERED ([username] ASC, [roomID] ASC, [bookdate] ASC),
    CONSTRAINT [CK_2] CHECK ([isActive]='否' OR [isActive]='是'),
    CONSTRAINT [FK_7] FOREIGN KEY ([roomID]) REFERENCES [dbo].[RoomInfo] ([roomID]),
    CONSTRAINT [FK_8] FOREIGN KEY ([username]) REFERENCES [dbo].[UserInfo] ([username]),
    CONSTRAINT [FK_9] FOREIGN KEY ([StaffID]) REFERENCES [dbo].[StaffInfo] ([StaffID])
);

-- 预定金额表
CREATE TABLE [dbo].[BookingMoney] (
    [username] CHAR (20) NOT NULL,
    [roomID]   CHAR (20) NOT NULL,
    [time]     DATETIME  NOT NULL,
    [money]    MONEY     NOT NULL,
    CONSTRAINT [PK_BookingMoney] PRIMARY KEY CLUSTERED ([username] ASC, [roomID] ASC, [time] ASC),
    CONSTRAINT [FK_19] FOREIGN KEY ([roomID]) REFERENCES [dbo].[RoomInfo] ([roomID]),
    CONSTRAINT [FK_20] FOREIGN KEY ([username]) REFERENCES [dbo].[UserInfo] ([username])
);

-- 取消预订表
CREATE TABLE [dbo].[CancelBooking] (
    [username] CHAR (20) NOT NULL,
    [roomID]   CHAR (20) NOT NULL,
    [StaffID]  INT       NULL,
    [time]     DATETIME  DEFAULT (getdate()) NOT NULL,
    [refund]   MONEY     NOT NULL,
    CONSTRAINT [PK_CancelBooking] PRIMARY KEY CLUSTERED ([username] ASC, [roomID] ASC),
    CONSTRAINT [FK_16] FOREIGN KEY ([roomID]) REFERENCES [dbo].[RoomInfo] ([roomID]),
    CONSTRAINT [FK_17] FOREIGN KEY ([StaffID]) REFERENCES [dbo].[StaffInfo] ([StaffID]),
    CONSTRAINT [FK_18] FOREIGN KEY ([username]) REFERENCES [dbo].[UserInfo] ([username])
);

-- 入住记录表
CREATE TABLE [dbo].[CheckIn] (
    [username] CHAR (20) NOT NULL,
    [roomID]   CHAR (20) NOT NULL,
    [StaffID]  INT       NOT NULL,
    [time]     DATETIME  DEFAULT (getdate()) NOT NULL,
    [deposit]  MONEY     NOT NULL,
    CONSTRAINT [PK_CheckIn] PRIMARY KEY CLUSTERED ([username] ASC, [roomID] ASC, [StaffID] ASC),
    CONSTRAINT [FK_13] FOREIGN KEY ([roomID]) REFERENCES [dbo].[RoomInfo] ([roomID]),
    CONSTRAINT [FK_14] FOREIGN KEY ([StaffID]) REFERENCES [dbo].[StaffInfo] ([StaffID]),
    CONSTRAINT [FK_15] FOREIGN KEY ([username]) REFERENCES [dbo].[UserInfo] ([username])
);

-- 退房记录表
CREATE TABLE [dbo].[CheckOut] (
    [username] CHAR (20) NOT NULL,
    [roomID]   CHAR (20) NOT NULL,
    [StaffID]  INT       NOT NULL,
    [time]     DATETIME  DEFAULT (getdate()) NOT NULL,
    [refund]   MONEY     NOT NULL,
    CONSTRAINT [PK_CheckOut] PRIMARY KEY CLUSTERED ([username] ASC, [roomID] ASC, [StaffID] ASC),
    CONSTRAINT [FK_10] FOREIGN KEY ([roomID]) REFERENCES [dbo].[RoomInfo] ([roomID]),
    CONSTRAINT [FK_11] FOREIGN KEY ([username]) REFERENCES [dbo].[UserInfo] ([username]),
    CONSTRAINT [FK_12] FOREIGN KEY ([StaffID]) REFERENCES [dbo].[StaffInfo] ([StaffID])
);

-- 评论表
CREATE TABLE [dbo].[Comment] (
    [commentid] INT       NOT NULL,
    [username]  CHAR (20) NOT NULL,
    [roomID]    CHAR (20) NOT NULL,
    CONSTRAINT [PK_Comment] PRIMARY KEY CLUSTERED ([commentid] ASC, [username] ASC, [roomID] ASC),
    CONSTRAINT [FK_1] FOREIGN KEY ([commentid]) REFERENCES [dbo].[CommentDetail] ([commentid]),
    CONSTRAINT [FK_2] FOREIGN KEY ([roomID]) REFERENCES [dbo].[RoomInfo] ([roomID]),
    CONSTRAINT [FK_3] FOREIGN KEY ([username]) REFERENCES [dbo].[UserInfo] ([username])
);

-- 评论细节表
CREATE TABLE [dbo].[CommentDetail] (
    [commentid] INT      IDENTITY (1, 1) NOT NULL,
    [content]   TEXT     NOT NULL,
    [star]      INT      NOT NULL,
    [time]      DATETIME DEFAULT (getdate()) NOT NULL,
    CONSTRAINT [PK_CommentDetail] PRIMARY KEY CLUSTERED ([commentid] ASC)
);

-- 房间表
CREATE TABLE [dbo].[RoomInfo] (
    [roomID]    CHAR (20)     NOT NULL,
    [roomtype]  VARCHAR (50)  NOT NULL,
    [roomstate] VARCHAR (50)  NOT NULL,
    [note]      VARCHAR (MAX) NULL,
    [img]       IMAGE         NULL,
    CONSTRAINT [PK_RoomInfo] PRIMARY KEY CLUSTERED ([roomID] ASC),
    CONSTRAINT [FK_4] FOREIGN KEY ([roomstate]) REFERENCES [dbo].[RoomState] ([statename]),
    CONSTRAINT [FK_5] FOREIGN KEY ([roomtype]) REFERENCES [dbo].[RoomType] ([typename])
);

-- 房间状态表
CREATE TABLE [dbo].[RoomState] (
    [statename]  VARCHAR (50) NOT NULL,
    [isoccupied] NCHAR (1)    DEFAULT ('否') NOT NULL,
    CONSTRAINT [PK_RoomState] PRIMARY KEY CLUSTERED ([statename] ASC)
);

-- 房间类型表
CREATE TABLE [dbo].[RoomType] (
    [typename] VARCHAR (50) NOT NULL,
    [price]    MONEY        NOT NULL,
    CONSTRAINT [PK_RoomType] PRIMARY KEY CLUSTERED ([typename] ASC)
);

-- 员工信息表
CREATE TABLE [dbo].[StaffInfo] (
    [StaffID]  INT          IDENTITY (1, 1) NOT NULL,
    [name]     CHAR (10)    NOT NULL,
    [tele]     VARCHAR (50) NOT NULL,
    [password] CHAR (20)    NOT NULL,
    [position] VARCHAR (50) NOT NULL,
    CONSTRAINT [PK_StaffInfo] PRIMARY KEY CLUSTERED ([StaffID] ASC)
);

-- 用户信息表
CREATE TABLE [dbo].[UserInfo] (
    [username] CHAR (20) NOT NULL,
    [password] CHAR (20) NOT NULL,
    [viptype]  INT       NOT NULL,
    [id]       CHAR (20) NULL,
    [tele]     CHAR (20) NOT NULL,
    CONSTRAINT [PK_UserInfo] PRIMARY KEY CLUSTERED ([username] ASC),
    CONSTRAINT [FK_6] FOREIGN KEY ([viptype]) REFERENCES [dbo].[VIPType] ([viptype])
);

-- VIP类型表
CREATE TABLE [dbo].[VIPType] (
    [viptype]  INT          IDENTITY (1, 1) NOT NULL,
    [vipname]  VARCHAR (50) NOT NULL,
    [discount] FLOAT (53)   NOT NULL,
    CONSTRAINT [PK_VIPType] PRIMARY KEY CLUSTERED ([viptype] ASC)
);




SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[空闲房间信息] AS SELECT
    [房间信息].*
FROM
    dbo.[房间信息]
WHERE
    [房间信息].isoccupied = '否'
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[房间信息] AS SELECT
    RoomInfo.*, 
    RoomState.isoccupied, 
    RoomType.price
FROM
    dbo.RoomInfo
    INNER JOIN
    dbo.RoomState
    ON 
        RoomInfo.roomstate = RoomState.statename
    INNER JOIN
    dbo.RoomType
    ON 
        RoomInfo.roomtype = RoomType.typename
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[正在入住的用户列表] AS SELECT
    Booking.username, 
    UserInfo.viptype, 
    UserInfo.tele
FROM
    dbo.Booking
    INNER JOIN
    dbo.UserInfo
    ON 
        Booking.username = UserInfo.username
WHERE
    Booking.isActive = '是'
GO


CREATE PROCEDURE [dbo].[入住]
  @username AS char(20), 
  @roomid AS CHAR(20), 
  @staffid AS INT,
  @mon AS money
AS
BEGIN

  INSERT INTO CheckIn VALUES(@username, @roomid, @staffid, GETDATE(), @mon)
    
END

CREATE PROCEDURE [dbo].[取消预订]
  @username AS char(20), 
  @roomid AS CHAR(20), 
  @staffid AS INT,
  @refund AS money,
    @bookdate AS datetime
AS
BEGIN

  INSERT INTO CancelBooking VALUES(@username, @roomid, @staffid, GETDATE(), @refund)
    
    UPDATE Booking SET isActive='否' WHERE username=@username AND roomID=@roomid AND bookdate=@bookdate
    
END

CREATE PROCEDURE [dbo].[退房]
  @username AS char(20), 
  @roomid AS CHAR(20), 
  @staffid AS INT,
  @refund AS money
AS
BEGIN

  INSERT INTO CheckIn VALUES(@username, @roomid, @staffid, GETDATE(), @refund)
    
END

CREATE PROCEDURE [dbo].[预定]
  @username AS char(20), 
  @roomid AS CHAR(20), 
  @staffid AS INT,
  @fromdate AS DATETIME,
  @todate AS DATETIME
AS
BEGIN

  INSERT INTO Booking VALUES(@username, @roomid, @staffid, GETDATE(), @fromdate, @todate, '是')
    
END


INSERT INTO RoomState VALUES('被预定', '是'), ('空闲', '否'), ('已入住', '是')
GO

CREATE TRIGGER 插入预定记录同时修改房间状态 ON Booking AFTER INSERT AS BEGIN
    UPDATE RoomInfo SET RoomState='被预定' WHERE roomID IN (
        SELECT roomID FROM inserted
    )
END
GO

CREATE TRIGGER 插入入住记录同时修改房间状态 ON CheckIn AFTER INSERT AS BEGIN
    UPDATE RoomInfo SET RoomState='已入住' WHERE roomID IN (
        SELECT roomID FROM inserted
    )
END
GO

CREATE TRIGGER 插入退房记录同时修改房间状态 ON CheckOut AFTER INSERT AS BEGIN
    UPDATE RoomInfo SET RoomState='空闲' WHERE roomID IN (
        SELECT roomID FROM inserted
    )
END
GO

CREATE TRIGGER 插入取消预定记录同时修改房间状态 ON CancelBooking AFTER INSERT AS BEGIN
    UPDATE RoomInfo SET RoomState='空闲' WHERE roomID IN (
        SELECT roomID FROM inserted
    )
END
GO
