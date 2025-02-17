def compute_taxes(total: float):
    """
    Compute GST/QST from total (assuming total includes taxes).
    """
    rate_gst = 0.05
    rate_qst = 0.09975
    subtotal = total / (1 + rate_gst) / (1 + rate_qst)
    gst = subtotal * rate_gst
    qst = (subtotal + gst) * rate_qst
    return round(subtotal, 2), round(gst, 2), round(qst, 2)