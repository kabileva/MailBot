CREATE DEFINER = root@localhost PROCEDURE add_reply (
        IN recipient_id BIGINT,
        IN sender_id BIGINT,
	IN subject TEXT,
	IN sender_name VARCHAR(45),
	IN text TEXT,
	IN date_time DATETIME,
	IN sent INT
)
        insert into tbl_emails
        (
		reply_recipient_id,
		reply_sender_id,
		reply_subject,
		reply_sender_name,
		reply_text,
		reply_date_time,
		reply_sent
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
