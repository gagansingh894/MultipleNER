from detector_system import DetectorSystem

if __name__ == "__main__":
    test_data1 = '"MARKS AND SPENCERS LTD", "LONDON", "ICNAO02312", "LONDON, GREAT BRITAIN", "TOYS", "INTEL LLC", "M&S CORPORATION Limited", "LONDON, ENGLAND", "XYZ 13423 / ILD", "ABC/ICL/20891NC"'
    test_data2 = '"ICNAO02312", "XYZ 13423 / ILD", "ABC/ICL/20891NC"'
    test_data3 = "123456"
    test_data = [test_data1, test_data2, test_data3]

    detector_system = DetectorSystem()
    for data in test_data:
        detector_system.ingest_text(data)
        detector_system.run()
        print(detector_system.clusters)