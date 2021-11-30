from django.shortcuts import render
from .calculations import get_db_connection
from .calculations import dosage_erdomed, dosage_range_by_age_and_weight, age_to_months, dosage_ospen, dosage_ospamox, dosage_sumamed


def dosage(request):
    error_msg = ""
    result = ""

    sirups = get_db_connection()
    sirups = sirups.find()
    sirup_names = []
    for sirup in sirups:
        sirup_names.append(sirup["Name"])

    if request.method == "POST":
        if request.POST["age"] == "" or request.POST["weight"] == "":
            error_msg = "Zadejte obě hodnoty."
            return render(
                request, "dosage/dosage.html",
                dict(sirup_names=sirup_names, result=result, error_msg=error_msg)
            )

        if request.POST["age_units"] == "roky":
            age = age_to_months(float(request.POST["age"]))
        else:
            age = float(request.POST["age"])

        if request.POST["sirup"] == "ERDOMED":
            result = dosage_erdomed(float(request.POST["weight"]), age)
            return render(
                request, "dosage/dosage.html",
                dict(sirup_names=sirup_names, result=result, error_msg=error_msg)
            )
        elif request.POST["sirup"] == "OSPAMOX":
            result = dosage_ospamox(
                float(request.POST["weight"])
            )
            return render(
                request, "dosage/dosage.html",
                dict(sirup_names=sirup_names, result=result, error_msg=error_msg)
            )
        elif request.POST["sirup"] == "SUMAMED" or request.POST["sirup"] == "SUMAMED_FORTE":
            result = dosage_sumamed(
                float(request.POST["weight"]), request.POST["sirup"]
            )
            return render(
                request, "dosage/dosage.html",
                dict(sirup_names=sirup_names, result=result, error_msg=error_msg)
            )

        elif request.POST["sirup"] == "OSPEN_0,75" or request.POST["sirup"] == "OSPEN_0,4":
            result = dosage_ospen(
                float(request.POST["weight"]), age, request.POST["sirup"]
            )
            return render(
                request, "dosage/dosage.html",
                dict(sirup_names=sirup_names, result=result, error_msg=error_msg)
            )
        else:
            result = dosage_range_by_age_and_weight(
                age, float(request.POST["weight"]), request.POST["sirup"])
            return render(
                request, "dosage/dosage.html",
                dict(sirup_names=sirup_names, result=result, error_msg=error_msg)
            )

    return render(
        request, "dosage/dosage.html",
        dict(sirup_names=sirup_names, result=result, error_msg=error_msg)
    )
