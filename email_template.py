EMAIL_BODY_HEADER = """
<table width="100%" align="center" bgcolor="#f9f9fa" style="background:#f9f9fa;padding-top:12px;padding-right:12px;padding-left:12px;padding-bottom:12px;margin-top:0px;margin-bottom:30px;width:100%">
      <tbody><tr>
        <td align="center" valign="top" width="100%" style="max-width:700px;padding-top:12px;padding-bottom:24px">
          <table align="center" width="100%" style="max-width:700px;border-collapse:collapse;padding-top:0px;padding-bottom:0px">
            <tbody>
              <tr>
                <td align="center" style="line-height:150%;padding-left:20px;padding-right:20px">
                    <h3 style="display:inline-block;padding-top:0;color:#363959;font-family:sans-serif;padding-left:20px;padding-right:20px;margin-top:0;margin-bottom:0">Private Email Relay</h3>
                </td>
              </tr>
            <tr>
              <td align="center" style="line-height:150%;padding-left:20px;padding-right:20px">
                <p style="display:inline-block;padding-top:0;font-size:13px;color:#363959;font-family:sans-serif;padding-left:20px;padding-right:20px;margin-top:0;margin-bottom:0">
                  <strong>From:</strong> {email_from}
                </p>
              </td>
            </tr>
            <tr>
              <td align="center" style="line-height:150%;padding-left:20px;padding-right:20px">
                <p style="display:inline-block;padding-top:0;font-size:13px;color:#363959;font-family:sans-serif;padding-left:20px;padding-right:20px;margin-top:0;margin-bottom:0">
                  <strong>To:</strong> {email_to}
                </p>
              </td>
            </tr>
            <tr>
              <td align="center" style="line-height:150%;padding-left:20px;padding-right:20px">
                <p style="display:inline-block;padding-top:0;font-size:13px;color:#363959;font-family:sans-serif;padding-left:20px;padding-right:20px;margin-top:0;margin-bottom:0">
                  <strong><a href="{email_archive_url}" target="_blank">Download original from archive</a></strong>
                </p>
              </td>
            </tr>
          </tbody></table>
        </td>
      </tr>
    </tbody></table>
"""