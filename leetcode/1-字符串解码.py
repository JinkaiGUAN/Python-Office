    """https://leetcode-cn.com/leetbook/read/queue-stack/gdwjv/

    Returns:
        [type]: [description]
    """


from typing import List


class Solution:
    def decodeString(self, s: str) -> str:
        digit_stack = []
        letter_stack = []
        # res = []

        for char in s:
            if char.isdigit():
                digit_stack.append(char)
            elif char.isalpha() or char == '[':
                if char == '[':
                    digit_stack.append('[') # seperate the digit
                letter_stack.append(char)
            else:
                sub_string = self.get_substring(letter_stack)
                # num = int(digit_stack.pop())
                num = self.get_number(digit_stack)
                letter_stack.append(num * sub_string)
                # res.append(num * sub_string)

        return ''.join(letter_stack)

    def get_number(self, digit_stack: List) -> int:
        """This is used to get continus digit number."""
        # digit_stack.pop() # '['
        res = []
        d = digit_stack.pop()
        if d.isdigit():
            res.append(d)
        while len(digit_stack):
            digit = digit_stack.pop() 
            if digit == '[':
                digit_stack.append('[')
                break
            res.append(digit)

        return int(''.join(res[::-1]))

    def get_substring(self, letter_stack: List) -> str:
        sub_char = ']'
        sub_string = []
        while sub_char != '[':
            sub_char = letter_stack.pop()
            sub_string.append(sub_char)
        sub_string = ''.join(sub_string[:-1][::-1])
        return sub_string


print(Solution().decodeString("3[z]2[2[y]pq4[2[jk]e1[f]]]ef"))