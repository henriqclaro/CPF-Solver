import re
from typing import List

def unformat_cpf(cpf: str) -> str:
    # Verifica o formatdo do CPF e padroniza de maneira limpa
    pattern = r'([\d_ ]{3})[ \.]?([\d_ ]{3})[ \.]?([\d_ ]{3})[ \-]?([\d_ ]{2})'
    
    cpf_match = re.match(pattern, cpf)
    
    if cpf_match is None:
        raise ValueError('O formato do CPF está incorreto.')
    
    return ''.join(cpf_match.group(1, 2, 3, 4))

def format_cpf(body_cpf: str, verifiers_list: List[str]) -> str:
    # Formata o CPF com pontuação
    str_verifiers = ''.join(verifiers_list)
    formatted_cpf = f'{body_cpf[:3]}.{body_cpf[3:6]}.{body_cpf[6:9]}-{str_verifiers}'
    
    return formatted_cpf

def calculate_verifiers(cpf: str) -> List[str]:
    # Calcula os dígitos verificadores
    first_sum = 0
    second_sum = 0
    
    for i in range(9):
        digit = int(cpf[i])
        first_sum += digit * (10 - i)
        second_sum += digit * (11 - i)
    
    first_verifier = ((first_sum * 10) % 11) % 10
    
    second_sum += first_verifier * 2
    second_verifier = ((second_sum * 10) % 11) % 10
    
    return [str(first_verifier), str(second_verifier)]

def check_verifiers(given: List[str], calculated: List[str]) -> bool:
    # Checa se os verificadores batem ou estão vazios
    first_digit_match = (given[0] in ['_', ' ']) or (given[0] == calculated[0])
    second_digit_match = (given[1] in ['_', ' ']) or (given[1] == calculated[1])
    
    return first_digit_match and second_digit_match

def solve_cpf(cpf:str) -> None:
    # Calcula as possibilidades de CPFs válidos
    try:
        clean_cpf = unformat_cpf(cpf)
    except ValueError as e:
        print(f'Error: {e}')
        return
    
    hole_indexes = [i for i, char in enumerate(clean_cpf) if char in ['_', ' ']]
    body_hole_indexes = [i for i in hole_indexes if i < 9]
    
    total_missing_count = len(hole_indexes)
    body_missing_count =  len(body_hole_indexes)
    
    given_verifiers = [clean_cpf[9], clean_cpf[10]]
    
    # Solução para o caso de buracos nos verificadores 
    # Ou validação de CPF
    if body_missing_count == 0:
        if clean_cpf == clean_cpf[0] * 11:
            print('O CPF é inválido.')
            return
        
        calculated_verifiers = calculate_verifiers(clean_cpf)
        
        if check_verifiers(given_verifiers, calculated_verifiers):
            if total_missing_count == 0:
                print('O CPF é matematicamente válido.')
            else:
                formatted_cpf = format_cpf(clean_cpf, calculated_verifiers)
                print(formatted_cpf)
            return
        else:
            print('O CPF é inválido.')
        return
    
    # Solução para o caso de buracos no corpo do CPF
    cpf_list = list(clean_cpf)
    found_any = False
    
    for i in range(10 ** body_missing_count):
        iteration = f'{i:0{body_missing_count}d}'
        
        for i, digit in enumerate(iteration):
            cpf_list[body_hole_indexes[i]] = digit
        
        body_cpf = ''.join(cpf_list)
        
        if body_cpf[:9] == body_cpf[0] * 9:
            continue
        
        calculated_verifiers = calculate_verifiers(body_cpf)
        
        if check_verifiers(given_verifiers, calculated_verifiers):
            formatted_cpf = format_cpf(body_cpf, calculated_verifiers)
            print(formatted_cpf)
            found_any = True
    
    if not found_any:
        print('Nenhum CPF foi encontrado.')

if __name__ == '__main__':
    try:
        user_input = input('Insira o CPF a completar (use _ ou espaço):\n> ')
        solve_cpf(user_input)
    except KeyboardInterrupt:
        print('\nProgram interrupted by user.')