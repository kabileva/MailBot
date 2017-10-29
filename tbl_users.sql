create table tbl_users (
        user_id BIGINT UNIQUE AUTO_INCREMENT,
        user_name VARCHAR(45) NULL,
        user_email VARCHAR(45) NULL,
        user_token VARCHAR(45) NULL,
        user_FB_id BIGINT NULL,
        user_FB_name VARCHAR(45) NULL,
        PRIMARY KEY (user_id));

