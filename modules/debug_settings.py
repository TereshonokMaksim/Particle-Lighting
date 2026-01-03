import modules.data as data
import modules.settings as settings


def get_debug_texts() -> list[str]:
    '''
        You are allowed to edit this whatever you like \n
        But make sure to return list of strings that you would like to see
        
        Returns list of strings (as stated above)
    '''
    standart_return_data = "DEBUG ON"
    shadow_data = f"Shadow is {['off', 'on'][data.shadow_on]}"
    scattering_data = f"Scattering is at {settings.scattering * 100}%"
    return [standart_return_data, shadow_data, scattering_data]
