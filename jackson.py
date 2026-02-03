def jackson_is_a_silly_head(weirdness, handsomeness, dorkiness):
    if weirdness >= handsomeness and weirdness >= dorkiness:
        return "This dude is super weird"
    if handsomeness >= weirdness and handsomeness >= dorkiness:
        return "this guys is too pretty for his own good."
    if dorkiness >= weirdness and dorkiness >= handsomeness:
        return "this guys face is as plain as the one ring, but at least he doesn't repulse women."
    return "this dude is not special in any way."

result = jackson_is_a_silly_head(9, 7, 8)
print(result)