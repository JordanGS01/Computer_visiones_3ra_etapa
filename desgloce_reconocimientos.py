
def asig_valores_estados_reconocidos(reconocimientos):
    """This functon takes the recognition and, based on it string values, asing the correspond value to a new variable.
    This is to make future operations.
    reconocimientos(list): is where are the face recognition results"""
    # Asignation of variable values. This is to make the percentages of the statistics.
    Joy = 0
    Sorrow = 0
    Anger = 0
    Surprise = 0
    Under_Exposed = 0
    Blurred = 0
    Headwear = 0
    #_______Joy_______
    if reconocimientos[0].get("face_expressions").get('joy_likelihood') == 'VERY_UNLIKELY':
        pass
    elif reconocimientos[0].get("face_expressions").get("joy_likelihood") == "UNLIKELY":
        Joy += 1
    elif reconocimientos[0].get("face_expressions").get("joy_likelihood") == "POSSIBLE":
        Joy += 2
    elif reconocimientos[0].get("face_expressions").get("joy_likelihood") == "LIKELY":
        Joy += 3
    else:
        Joy += 4
    #_______Sorrow_______
    if reconocimientos[0].get("face_expressions").get('sorrow_likelihood') == 'VERY_UNLIKELY':
        pass
    elif reconocimientos[0].get("face_expressions").get("sorrow_likelihood") == "UNLIKELY":
        Sorrow += 1
    elif reconocimientos[0].get("face_expressions").get("sorrow_likelihood") == "POSSIBLE":
        Sorrow += 2
    elif reconocimientos[0].get("face_expressions").get("sorrow_likelihood") == "LIKELY":
        Sorrow += 3
    else:
        Sorrow += 4
    #_______Anger_______
    if reconocimientos[0].get("face_expressions").get("anger_likelihood") == "VERY_UNLIKELY":
        pass
    elif reconocimientos[0].get("face_expressions").get("anger_likelihood") == "UNLIKELY":
        Anger += 1
    elif reconocimientos[0].get("face_expressions").get("anger_likelihood") == "POSSIBLE":
        Anger += 2
    elif reconocimientos[0].get("face_expressions").get("anger_likelihood") == "LIKELY":
        Anger += 3
    else:
        Anger += 4
    #_______Surprise_______
    if reconocimientos[0].get("face_expressions").get("surprise_likelihood") == "VERY_UNLIKELY":
        pass
    elif reconocimientos[0].get("face_expressions").get("surprise_likelihood") == "UNLIKELY":
        Surprise += 1
    elif reconocimientos[0].get("face_expressions").get("surprise_likelihood") == "POSSIBLE":
        Surprise += 2
    elif reconocimientos[0].get("face_expressions").get("surprise_likelihood") == "LIKELY":
        Surprise += 3
    else:
        Surprise += 4
    #_______Under_exposed_______
    if reconocimientos[0].get("face_expressions").get("under_exposed_likelihood") == "VERY_UNLIKELY":
        pass
    elif reconocimientos[0].get("face_expressions").get("under_exposed_likelihood") == "UNLIKELY":
        Under_Exposed += 1
    elif reconocimientos[0].get("face_expressions").get("under_exposed_likelihood") == "POSSIBLE":
        Under_Exposed += 2
    elif reconocimientos[0].get("face_expressions").get("under_exposed_likelihood") == "LIKELY":
        Under_Exposed += 3
    else:
        Under_Exposed += 4
    #_______Blurred_______
    if reconocimientos[0].get("face_expressions").get("blurred_likelihood") == "VERY_UNLIKELY":
        pass
    elif reconocimientos[0].get("face_expressions").get("blurred_likelihood") == "UNLIKELY":
        Blurred += 1
    elif reconocimientos[0].get("face_expressions").get("blurred_likelihood") == "POSSIBLE":
        Blurred += 2
    elif reconocimientos[0].get("face_expressions").get("blurred_likelihood") == "LIKELY":
        Blurred += 3
    else:
        Blurred += 4
    #_______Headwear_______
    if reconocimientos[0].get("face_expressions").get("headwear_likelihood") == "VERY_UNLIKELY":
        pass
    elif reconocimientos[0].get("face_expressions").get("headwear_likelihood") == "UNLIKELY":
        Headwear += 1
    elif reconocimientos[0].get("face_expressions").get("headwear_likelihood") == "POSSIBLE":
        Headwear += 2
    elif reconocimientos[0].get("face_expressions").get("headwear_likelihood") == "LIKELY":
        Headwear += 3
    else:
        Headwear += 4

    dic_reconocimiento =  {"Joy":Joy, "Sorrow":Sorrow, "Anger":Anger,"Surprise":Surprise,
                           "Under_Exposed":Under_Exposed,"Blurred":Blurred,"Headwear":Headwear}
    return dic_reconocimiento