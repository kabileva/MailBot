CREATE DEFINER = root@localhost PROCEDURE add_email (
        IN recipient_id BIGINT,
        IN sender_id BIGINT,
	IN subject TEXT,
	IN sender_name VARCHAR(45),
	IN text TEXT,
	IN date_time DATETIME
)
        insert into tbl_emails
        (
		email_recipient_id,
		email_sender_id,
		email_subject,
		email_sender_name,
		email_text,
		email_date_time
        )
        values
	(
		recipient_id,
		sender_id,
		subject,
		sender_name,
		text,
		date_time
        );
    
