import base62 as bs

l_url= int(input())

def longtoshort(m_long):
        
    m_short= bs.encode(m_long)

    return m_short

def shorttolong(m_short):
        
    m_long= bs.decode(m_short)

    return m_long

s_url=longtoshort(l_url)
print(s_url)



