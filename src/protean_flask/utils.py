""" Utility functions used by Protean Flask"""


def immutable_dict_2_dict(imm_dict):
    """ Function to convert an Immutable Dictionary to a Mutable one
    Convert multi valued and keys ending with [] to lists
    """
    m_dict = {}

    for key, val in imm_dict.to_dict(flat=False).items():
        if len(val) > 1 or key.endswith('[]'):
            m_dict[key.strip('[]')] = val
        else:
            m_dict[key] = val[0]

    return m_dict
