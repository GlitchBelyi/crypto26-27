from collections import Counter
import sys

def calculate_im(text_block):

    n = len(text_block)
    
    if n <= 1:
        return 0.0
        
    counter = Counter(text_block)
    
    _sum = sum(count * (count - 1) for count in counter.values())
    
    return _sum / (n * (n - 1))

if __name__ == '__main__':

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        text = f.read()

    print("|Довжина ключа | Усереднений індекс відповідності|")
    print("|--------------|--------------------------|")

    dict_of_im = {}

    for r in range(2, 31):
        im_values = []
        

        for j in range(r):
            block = text[j::r] 
            
            ic = calculate_im(block)
            im_values.append(ic)
            
        avg_im = sum(im_values) / r
        dict_of_im[r] = avg_im
        
    dict_of_im = dict(sorted(dict_of_im.items(), key=lambda item: item[1], reverse=True))   

    for r, avg_im in dict_of_im.items():    
        print(f"|{r:<14} | {avg_im:.6f}|")