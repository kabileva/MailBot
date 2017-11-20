CREATE DEFINER = root@localhost PROCEDURE add_email (
        IN recipient_id BIGINT,
        IN sender_id VARCHAR(45),
	IN subject TEXT,
	IN sender_name VARCHAR(45),
	IN text TEXT,
	IN date_time DATETIME,
	IN sent INT
)
        insert into tbl_emails
        (
		email_recipient_id,
		email_sender_id,
		email_subject,
		email_sender_name,
		email_text,
		email_date_time,
		email_sent
        )
        values
	(
		recipient_id,
		sender_id,
		subject,
		sender_name,
		text,
		date_time,
		sent
        );
    
