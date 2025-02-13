begin
  -- Allow SMTP access for user ADMIN
  dbms_network_acl_admin.append_host_ace(
    host =>'smtp.us-ashburn-1.oraclecloud.com',
    lower_port => 587,
    upper_port => 587,
    ace => xs$ace_type(
      privilege_list => xs$name_list('SMTP'),
    principal_name => 'ADMIN',
    principal_type => xs_acl.ptype_db));
end;
/