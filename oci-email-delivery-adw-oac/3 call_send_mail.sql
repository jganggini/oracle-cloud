DECLARE
  I_MSG_TO VARCHAR2(200);
  I_MSG_SUBJECT VARCHAR2(200);
  I_MSG VARCHAR2(2000);
BEGIN
  I_MSG_TO := 'correo@dominio.com';
  I_MSG_SUBJECT := 'Salary';
  I_MSG := 'https://demoanalysis-idlhjo6dp3bd-ia.analytics.ocp.oraclecloud.com/ui/analytics/saw.dll?Dashboard&PortalPath=%2Fusers%2Fjoel.ganggini%40oracle.com%2FPanel&Page=p%C3%A1gina%201&PageIdentifier=k4q01q67s8dkcmuu&BookmarkState=eepl285gvpa9vdu1p3b7p2rn5u';

  SP_SEND_MAIL(
    I_MSG_TO => I_MSG_TO,
    I_MSG_SUBJECT => I_MSG_SUBJECT,
    I_MSG => I_MSG
  );
--rollback; 
END;
