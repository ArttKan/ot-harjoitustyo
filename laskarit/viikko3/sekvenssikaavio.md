
 sequenceDiagram
    main->>HKLLaitehallinto: laitehallinto
    main->>rautatietori: Lataajalaite()
    main->>ratikka6: Lukijalaite()
    main->>bussi244: Lukijalaite()
    main->>HKLLaitehallinto: lisaa_lataaja(rautatietori)
    main->>HKLLaitehallinto: lisaa_lataaja(ratikka6)
    main->>HKLLaitehallinto: lisaa_lataaja(bussi244)
    main->>lippu_luukku: Kioski()
    lippu_luukku->>kallen_kortti: osta_matkakortti("Kalle")
    rautatietori->>kallen_kortti: lataa_arvoa(kallen_kortti, 3)
    ratikka6->>kallen_kortti: osta_lippu(kallen_kortti, 0)
    bussi244->>kallen_kortti: osta_lippu(kallen_kortti, 2)
