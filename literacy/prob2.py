import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from literacy.prob import problem

sample_problem = r"""
        다음 코드는 스크래치 형태로 팰린드롬을 검사하는 코드입니다.
        팰린드롬은 앞으로 읽으나 뒤로 읽으나 같은 문자열을 말합니당.
        ```scratch
        // Scratch로 작성된 팰린드롬 검사 프로그램

        when [space v] clicked
            set [userInput v] to [ask] and wait
            change background color by [10]
            
            // 사용자 입력을 소문자로 변환
            set [input lower v] to (lowerletters (userInput))
            
            // 길이 체크
            if <(length of) (input lower v) < 2> then
                say [This text is too short to be a word.] for (1) seconds
                broadcast [OK]
                
            repeat (length of) (input lower v)
                if <not ((input lower v) at (index)) = ((input lower v) at ((index) + (1)))> then
                    broadcast [This text is not a palindrome.]
                    broadcast [OK]
                    stop
                
            broadcast [This text is a palindrome.]
            broadcast [OK]
        end
        ```
        """


problem(sample_problem, 'prob2')