def volt_to_mm(volt, x_or_y):
    m, b = _return_m_b(x_or_y, 'volt_to_mm')
    mm = m*volt + b
    return mm

def mm_to_volt(mm, x_or_y):
    m, b = _return_m_b(x_or_y, 'mm_to_volt')
    volt = m*mm + b
    return volt

def _return_m_b(x_or_y, what_to_what):
    if x_or_y == 'x':
        # m = -0.012546660621089764
        # b = -0.06912179728030933
        m = 0.0125475
        b = 0.06922331

    elif x_or_y == 'y':
        # m = -0.012882209183473516
        # b = -0.06530445662203191
        m = 0.01288427
        b = 0.06470308

    if what_to_what == 'mm_to_volt':
        return m, b
    elif what_to_what == 'volt_to_mm':
        return 1/m, -b/m