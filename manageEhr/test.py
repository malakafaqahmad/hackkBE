from ehr_manager import EHRManager

if __name__ == "__main__":
    manager = EHRManager()

    # full  = manager.get_patient_full_record("p1")
    # print(full)

    p1 = manager.get_all_patient_ehr_data("p1")
    print(p1)