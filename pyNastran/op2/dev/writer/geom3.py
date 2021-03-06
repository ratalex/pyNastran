from __future__ import absolute_import
from struct import pack, Struct
from collections import defaultdict

from .geom1 import write_geom_header, close_geom_table

def write_geom3(op2, op2_ascii, obj, endian=b'<'):
    if not hasattr(obj, 'loads') and not hasattr(obj, 'load_combinations'):
        return
    loads_by_type = defaultdict(list)
    for unused_load_id, loads in obj.loads.items():
        for load in loads:
            loads_by_type[load.type].append(load)
    for unused_load_id, loads in obj.load_combinations.items():
        for load in loads:
            loads_by_type[load.type].append(load)
    for unused_load_id, load in obj.tempds.items():
        loads_by_type[load.type].append(load)

    # return if no supported cards are found
    cards_to_skip = ['LOAD']
    supported_cards = [
        'FORCE', 'FORCE1', 'FORCE2', 'MOMENT', 'MOMENT1', 'MOMENT2',
        'PLOAD', 'PLOAD1', 'PLOAD2', 'PLOAD4', 'PLOADX1',
        'GRAV', 'SLOAD', 'RFORCE',
        #'ACCEL', 'ACCEL1',
        'TEMP', 'TEMPP1', 'QBDY1', 'QBDY2', 'QBDY3', 'QVOL',
    ]
    is_loads = False
    for load_type in sorted(loads_by_type.keys()):
        if load_type in supported_cards:
            is_loads = True
            break
        elif load_type in cards_to_skip:
            continue
        obj.log.warning('skipping GEOM3-%s' % load_type)
    #else:
        #return

    if not is_loads:
        return
    write_geom_header(b'GEOM3', op2, op2_ascii)
    itable = -3
    for load_type, loads in sorted(loads_by_type.items()):
        if load_type in ['SPCD']: # not a GEOM3 load
            continue
        elif load_type in cards_to_skip:
            obj.log.warning('skipping GEOM3-%s' % load_type)
            continue

        #elif load_type not in supported_cards:
            #continue

        try:
            nbytes = write_card(op2, op2_ascii, load_type, loads, endian)
        except:
            obj.log.error('failed GEOM3-%s' % load_type)
            raise
        op2.write(pack('i', nbytes))

        itable -= 1
        data = [
            4, itable, 4,
            4, 1, 4,
            4, 0, 4]
        op2.write(pack('9i', *data))
        op2_ascii.write(str(data) + '\n')

    #-------------------------------------
    #print('itable', itable)
    close_geom_table(op2, op2_ascii, itable)

    #-------------------------------------

def write_card(op2, op2_ascii, load_type, loads, endian):
    nloads = len(loads)
    if load_type == 'FORCE':
        key = (4201, 42, 18)
        nfields = 7
        spack = Struct(endian + b'3i 4f')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            data = [load.sid, load.node_id, load.Cid(), load.mag] + list(load.xyz)
            op2_ascii.write('  FORCE data=%s\n' % str(data))
            op2.write(spack.pack(*data))
    elif load_type == 'FORCE1':
        key = (4001, 40, 20)
        nfields = 5
        spack = Struct(endian + b'iifii')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, node, mag, n1, n2) = out
            data = [load.sid, load.node_id, load.mag, load.G1(), load.G2()]
            op2_ascii.write('  FORCE1 data=%s\n' % str(data))
            op2.write(spack.pack(*data))
    elif load_type == 'FORCE2':
        key = (4101, 41, 22)
        nfields = 7
        spack = Struct(endian + b'iif4i')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, node_id, mag, n1, n2, n3, n4) = out
            data = [load.sid, load.node_id, load.mag,
                    load.G1(), load.G2(), load.G3(), load.G4()]
            op2_ascii.write('  FORCE2 data=%s\n' % str(data))
            op2.write(spack.pack(*data))

    elif load_type == 'MOMENT':
        key = (4801, 48, 19)
        nfields = 7
        spack = Struct(endian + b'3i 4f')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            data = [load.sid, load.node_id, load.Cid(), load.mag] + list(load.xyz)
            op2_ascii.write('  MOMENT data=%s\n' % str(data))
            op2.write(spack.pack(*data))
    elif load_type == 'MOMENT1':
        key = (4601, 46, 21)
        nfields = 5
        spack = Struct(endian + b'iifii')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, node, mag, n1, n2) = out
            data = [load.sid, load.node_id, load.mag, load.G1(), load.G2()]
            op2_ascii.write('  MOMENT1 data=%s\n' % str(data))
            op2.write(spack.pack(*data))
    elif load_type == 'MOMENT2':
        key = (4701, 47, 23)
        nfields = 7
        spack = Struct(endian + b'iif4i')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, node_id, mag, n1, n2, n3, n4) = out
            data = [load.sid, load.node_id, load.mag,
                    load.G1(), load.G2(), load.G3(), load.G4()]
            op2_ascii.write('  MOMENT2 data=%s\n' % str(data))
            op2.write(spack.pack(*data))

    elif load_type == 'GRAV':
        key = (4401, 44, 26)
        nfields = 7
        #(sid, cid, a, n1, n2, n3, mb) = out
        spack = Struct(endian + b'ii4fi')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            data = [load.sid, load.Cid(), load.scale] + list(load.N) + [load.mb]
            op2_ascii.write('  GRAV data=%s\n' % str(data))
            op2.write(spack.pack(*data))
    elif load_type == 'PLOAD':
        key = (5101, 51, 24)
        nfields = 6
        spack = Struct(endian + b'i f 4i')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, pressure, n1, n2, n3, n4) = out
            nids = list(load.node_ids)
            if len(nids) == 3:
                nids.append(0)
            data = [load.sid, load.pressure] + nids
            op2_ascii.write('  PLOAD data=%s\n' % str(data))
            op2.write(spack.pack(*data))
    elif load_type == 'PLOAD1':
        key = (6909, 69, 198)
        nfields = 8
        spack = Struct(endian + b'4i4f')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, eid, load_type, scale, x1, p1, x2, p2) = out
            load_typei = load.valid_types.index(load.load_type) + 1 # 1-based
            scale = load.valid_scales.index(load.scale) + 1
            data = [load.sid, load.eid, load_typei, scale,
                    load.x1, load.p1, load.x2, load.p2]
            op2_ascii.write('  PLOAD1 data=%s\n' % str(data))
            op2.write(spack.pack(*data))
    elif load_type == 'PLOAD2':
        key = (6802, 68, 199)
        nfields = 3
        spack = Struct(endian + b'ifi')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, p, eid) = out
            for eid in load.eids:
                data = [load.sid, load.pressure, eid]
                op2_ascii.write('  PLOAD2 data=%s\n' % str(data))
                op2.write(spack.pack(*data))
    elif load_type == 'PLOAD4': # msc
        key = (7209, 72, 299)
        nfields = 16
        spack = Struct(endian + b'2i 4f 3i 3f 8s 8s')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #surf_or_line = surf_or_line.rstrip().decode('latin1')
            #line_load_dir = line_load_dir.rstrip().decode('latin1')
            #if line_load_dir == '':
                ## TODO: not 100%
                #line_load_dir = 'NORM'

            ## forces NX pload4 function to get called if it should be
            #assert surf_or_line in ['SURF', 'LINE']
            #assert line_load_dir in ['LINE', 'X', 'Y', 'Z', 'TANG', 'NORM'], 'line_load_dir=%r' % line_load_dir

            #self.pressures = np.asarray(pressures, dtype='float64')
            #self.nvector = nvector
            #self.surf_or_line = surf_or_line
            #self.line_load_dir = line_load_dir
            pressures = list(load.pressures)
            g1 = load.g1 if load.g1 is not None else 0
            g34 = load.g34 if load.g34 is not None else 0
            cid = load.cid if load.cid is not None else 0
            nids_cid = [g1, g34, cid]
            nvector = list(load.nvector)
            assert len(load.pressures) == 4, load.pressures
            assert None not in nids_cid, nids_cid

            pnn = pressures + nids_cid + nvector
            for eid in load.eids:
                #(sid, eid, p1, p2, p3, p4, g1, g34, cid, n1, n2, n3, surf_or_line, line_load_dir) = out
                surf_or_line = load.surf_or_line.encode('ascii')
                line_load_dir = load.line_load_dir.encode('ascii')
                data = [load.sid, eid] + pnn + [surf_or_line, line_load_dir]

                assert None not in data, data
                op2_ascii.write('  PLOAD4 data=%s\n' % str(data))
                op2.write(spack.pack(*data))
    elif load_type == 'PLOADX1':
        key = (7309, 73, 351)
        nfields = 7
        spack = Struct(endian + b'2i2f iif')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, eid, pa, pb, ga, gb, theta) = out
            data = [load.sid, load.eid, load.pa, load.pb, load.ga, load.gb, load.theta]
            op2_ascii.write('  PLOADX1 data=%s\n' % str(data))
            op2.write(spack.pack(*data))
    elif load_type == 'SLOAD':
        key = (5401, 54, 25)
        nfields = 3
        spack = Struct(endian + b'2i f')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            for nid, mag in zip(load.nodes, load.mags):
                #(sid, nid, scale_factor) = out
                data = [load.sid, nid, mag]
                op2_ascii.write('  SLOAD data=%s\n' % str(data))
                op2.write(spack.pack(*data))
    elif load_type == 'RFORCE':
        key = (5509, 55, 190)
        nfields = 10
        spack = Struct(endian + b'3i 4f ifi')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #self.idrf = idrf
            #sid, nid, cid, a, r1, r2, r3, method, racc, mb = data
            #scale = 1.0
            data = [load.sid, load.nid, load.cid, load.scale] + load.r123 + [
                load.method, load.racc, load.mb]
            assert load.idrf == 0, load
            op2_ascii.write('  RFORCE data=%s\n' % str(data))
            op2.write(spack.pack(*data))
    elif load_type == 'TEMP':
        key = (5701, 57, 27)
        nfields = 3
        spack = Struct(endian + b'iif')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            for nid, temp in sorted(load.temperatures.items()):
                #(sid, g, T) = out
                data = [load.sid, nid, temp]
                op2_ascii.write('  TEMP data=%s\n' % str(data))
                op2.write(spack.pack(*data))
    elif load_type == 'QVOL':
        key = (2309, 23, 416)
        nfields = 4
        spack = Struct(endian + b'if2i')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, qvol, cntrlnd, eid) = out
            for eid in load.elements:
                data = [load.sid, load.qvol, load.control_point, eid]
                op2_ascii.write('  QVOL data=%s\n' % str(data))
                op2.write(spack.pack(*data))
    elif load_type == 'QBDY1':
        key = (4509, 45, 239)
        nfields = 3
        spack = Struct(endian + b'ifi')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, q0, eid) = out
            for eid in load.eids:
                data = [load.sid, load.qflux, eid]
                op2_ascii.write('  QBDY1 data=%s\n' % str(data))
                op2.write(spack.pack(*data))
    elif load_type == 'QBDY2':
        key = (4909, 49, 240)
        nfields = 10
        spack = Struct(endian + b'ii8f')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, eid, q1, q2, q3, q4, q5, q6, q7, q8) = out
            qflux = list(load.qfluxs)
            nflux = len(qflux)
            if nflux < 8:
                qflux = qflux + [0.] * (8 - nflux)
            data = [load.sid, load.eid] + qflux
            op2_ascii.write('  QBDY2 data=%s\n' % str(data))
            op2.write(spack.pack(*data))
    elif load_type == 'QBDY3':
        key = (2109, 21, 414)
        nfields = 4
        spack = Struct(endian + b'ifii')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #(sid, q0, cntrlnd, eid) = out
            for eid in load.eids:
                data = [load.sid, load.q0, load.cntrlnd, eid]
                op2_ascii.write('  QBDY3 data=%s\n' % str(data))
                op2.write(spack.pack(*data))
    elif load_type == 'TEMPP1':
        key = (8109, 81, 201)
        nfields = 6
        spack = Struct(endian + b'2i 4f')
        nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        for load in loads:
            #sid, eid, t, tprime, ts1, ts2 = data
            data = [load.sid, load.eid, load.tbar, load.tprime] + load.t_stress
            op2_ascii.write('  TEMPP1 data=%s\n' % str(data))
            op2.write(spack.pack(*data))
    #elif load_type == 'ACCEL1':
        #key = (7401,74,601)
        #nfields = 3
        #spack = Struct(endian + b'2i f')
        #nbytes = write_header(load_type, nfields, nloads, key, op2, op2_ascii)
        #for load in loads:
            #1 SID    I Load set identification number
            #2 CID    I Coordinate system identification number
            #3 A     RS Acceleration vector scale factor
            #4 N(3)  RS Components of a vector coordinate system defined by CID
            #7 GRIDID I Grid ID or THRU or BY code
            #Words 7 repeats until (-1) occurs.
            #for nid, mag in zip(load.nodes, load.mags):
                #data = [load.sid, nid, mag]
                #op2_ascii.write('  SLOAD data=%s\n' % str(data))
                #op2.write(spack.pack(*data))
    else:  # pragma: no cover
        load0 = loads[0]
        raise NotImplementedError(load0)
    return nbytes

def write_header(name, nfields, nloads, key, op2, op2_ascii):
    nvalues = nfields * nloads + 3 # +3 comes from the keys
    nbytes = nvalues * 4
    op2.write(pack('3i', *[4, nvalues, 4]))
    op2.write(pack('i', nbytes)) #values, nbtyes))

    op2.write(pack('3i', *key))
    op2_ascii.write('%s %s\n' % (name, str(key)))
    return nbytes
