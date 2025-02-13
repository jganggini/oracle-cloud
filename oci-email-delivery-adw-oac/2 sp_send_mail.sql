create or replace PROCEDURE sp_send_mail (
  i_msg_to        VARCHAR2,
  i_msg_subject   VARCHAR2,
  i_msg           VARCHAR2)
IS

  mail_conn utl_smtp.connection;
  v_username      VARCHAR2(1000)   := 'ocid1.user.oc1..aaaaaaaawbh6e75hxk3st7athfu3ocaj76sbyewl5bf7f4pef6hs23aje7eq@ocid1.tenancy.oc1..aaaaaaaavl2ndgiiefoo2u4a7atlq2czcwyiu5zzb6rzwwpeyt5o2xmtaxwa.k9.com';
  v_passwd        VARCHAR2(50)     := 'opK+2W)fmru#5Z8]erP{';
  v_msg_from      VARCHAR2(50)     := 'correo@correo.com';
  v_mailhost      VARCHAR2(50)     := 'smtp.email.us-ashburn-1.oci.oraclecloud.com';

  l_boundary      VARCHAR2(50)     := '----=*#abc1234321cba#*=';
  v_count         INTEGER;
  v_total         INTEGER;
  v_rcpt          VARCHAR2(500);
  v_html          CLOB             := NULL;
BEGIN
  mail_conn := UTL_smtp.open_connection(v_mailhost, 587);
  utl_smtp.starttls(mail_conn);

  UTL_SMTP.AUTH(mail_conn, v_username, v_passwd, schemes => 'PLAIN');

  utl_smtp.mail(mail_conn, v_msg_from);

  v_count   := 0;
  v_total   := instr(i_msg_to, ','); 

  v_html    := 
  '<html>
  <head>
  <style>
    table { border-collapse: collapse; width: 100%; border:1px #D9D9D9 solid; border:0px; padding:0px; }
    th, td { text-align: left; padding: 8px; background:#FFFFFF; border:0px; padding:0px; }
    tr:nth-child(even){ background-color: #eaeaea }
    th { background-color: red; color: white; border:1px red solid; }
  </style>
  </script>
  </head>
  <body style="background:#F7F7F7; text-decoration:none;">
  <table width="100%" cellspacing="0" cellpadding="0">
    <tbody>
      <tr>
        <td>;</td>
        <td style="width:900px;">
          <table width="100%" cellspacing="0" cellpadding="0">
            <tbody>
              <tr>
                <td style="min-width:700px;">
                  <div style="padding:20px 0 0 0; background:#F7F7F7;">
                    <img style="display:block;" src="https://raw.githubusercontent.com/jganggini/oci-email-delivery/main/send-email-by-adw-and-oac/src/img/banner_email.png" width="100%" height="100%"/>
                  </div>
                  <div style="color:#8E8E8E; border:1px #12161c solid; border-top:0px; padding:10px; font-family:Verdana; font-size:12px;">
                    <div style="margin:0 0 10px 5px; background:#F3F3F3; padding:10px; font-size:12px; min-height:15px;">
                      <!-- Variable -->
                      '|| i_msg_subject ||'
                    </div>
                    <div style="margin:0 0 10px 5px; text-align: center;">
                      <!-- Variable -->
                      <a style="font-size:11px; color:#12161c;" href="'|| i_msg ||'">click para abrir el reporte</a>
                    </div>
                    <div style="margin:10px 0 0 0; background:#12161c; text-align:right; color:#FFFFFF; padding:10px; font-size:11px; height:15px;">
                      Developed by <a style="font-size:11px; color:#FFFFFF;" href="mailto:corre@dominio.com">correo@dominio.com</a>
                    </div>
                  </div>
                 </td>
              </tr>
            </tbody>
          </table>
          </td>
        <td>;</td>
      </tr>
    </tbody>
  </table>
  </body>
  </html>';
  --DBMS_OUTPUT.PUT_LINE(v_html);

  IF (v_total = 0) THEN
    utl_smtp.rcpt(mail_conn, i_msg_to);
  ELSE
    WHILE(v_total > 0) LOOP
      v_rcpt     := SUBSTR(i_msg_to, v_count+1, v_total - v_count - 1);
      utl_smtp.rcpt(mail_conn, v_rcpt);
      v_count    := v_total;
      v_total    := instr(i_msg_to, ',', v_count + 1);  
    END LOOP;
  END IF;

  UTL_SMTP.open_data(mail_conn);
  UTL_SMTP.write_data(mail_conn, 'Date: ' || TO_CHAR(SYSDATE, 'DD-MON-YYYY HH24:MI:SS') || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, 'To: ' || i_msg_to || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, 'From: ' || v_msg_from || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, 'Subject: ' || i_msg_subject || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, 'Reply-To: ' || i_msg_to || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, 'MIME-Version: 1.0' || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, 'Content-Type: multipart/alternative; boundary="' || l_boundary || '"' || UTL_TCP.crlf || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, '--' || l_boundary || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, 'Content-Type: text/html; charset="iso-8859-1"' || UTL_TCP.crlf || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, v_html);
  UTL_SMTP.write_data(mail_conn, UTL_TCP.crlf || UTL_TCP.crlf);
  UTL_SMTP.write_data(mail_conn, '--' || l_boundary || '--' || UTL_TCP.crlf);
  UTL_SMTP.close_data(mail_conn);
  UTL_SMTP.quit(mail_conn);

EXCEPTION
  WHEN UTL_smtp.transient_error OR UTL_smtp.permanent_error THEN
    UTL_smtp.quit(mail_conn);
    dbms_output.put_line(sqlerrm);
  WHEN OTHERS THEN
    UTL_smtp.quit(mail_conn);
    dbms_output.put_line(sqlerrm);
END;