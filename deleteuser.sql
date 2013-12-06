SET @userId = (SELECT id FROM auth_user WHERE username = '<<<<<the-user-you-want-to-delete>>>>>');
DELETE FROM forum_actionrepute WHERE user_id = @userId;
DELETE FROM forum_action WHERE user_id = @userId;
DELETE FROM forum_validationhash WHERE user_id = @userId;
DELETE FROM forum_subscriptionsettings WHERE user_id = @userId;
DELETE FROM forum_userproperty WHERE user_id = @userId;
DELETE FROM forum_user WHERE user_ptr_id = @userId;
DELETE FROM auth_user WHERE id = @userId;