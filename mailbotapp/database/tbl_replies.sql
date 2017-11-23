create table tbl_replies (
        reply_id BIGINT UNIQUE AUTO_INCREMENT,
        reply_recipient_id VARCHAR(45) NULL,
        reply_sender_id BIGINT NULL,
        reply_subject TEXT NULL,
        reply_sender_name VARCHAR(45) NULL,
        reply_text TEXT NULL,
        reply_date_time DATETIME NULL,
	    reply_sent INT NULL,
        FOREIGN KEY (reply_sender_id)
                REFERENCES tbl_users(user_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        PRIMARY KEY (reply_id)); 

