from django.conf import settings
import random
import ghasedak_sms

# OTP with ghasedak_sms
def send_otp_ghasedak(phone_number): 
    otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    newotpcommand = ghasedak_sms.SendOtpInput(
        send_date=None,
        receptors=[
            ghasedak_sms.SendOtpReceptorDto(
                mobile=f'{phone_number}',
                # client_reference_id='client_ref_id'
            )
        ],
        template_name='Ghasedak',
        inputs=[
            ghasedak_sms.SendOtpInput.OtpInput(param='Code', value=f'{otp_code}'),
            ghasedak_sms.SendOtpInput.OtpInput(param='Name', value='name')
        ],
        udh=False
    )
    sms_api = ghasedak_sms.Ghasedak(api_key=settings.API_KEY)
    response = sms_api.send_otp_sms(newotpcommand)
    print(response)
    if response['statusCode'] == 200:
        return otp_code
    return None