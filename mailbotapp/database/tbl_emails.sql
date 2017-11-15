create table tbl_emails (
        email_id BIGINT UNIQUE AUTO_INCREMENT, --here just because primary id is needed
        email_recipient_id BIGINT NULL, -- how we actually recognize whom the email belongs to
        email_sender_id BIGINT NULL,
        email_subject TEXT NULL,
        email_sender_name VARCHAR(45) NULL,
        email_text TEXT NULL,
        email_date_time DATETIME NULL,
	email_sent INT NULL,
        FOREIGN KEY (email_id)
                REFERENCES tbl_users(user_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
        PRIMARY KEY (email_id));
