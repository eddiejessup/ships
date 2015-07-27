from __future__ import print_function, division
from ahoy import directions, measurers, rudders, positions, swimmers


class Agents(object):

    def __init__(self, directions, rudder_sets):
        self.directions = directions
        self.rudder_sets = rudder_sets

    def iterate(self, dt):
        for ruds in self.rudder_sets:
            self.directions = ruds.rotate(self.directions, dt)

    def get_chi(self):
        for ruds in self.rudder_sets:
            if ruds.is_chemotactic():
                return ruds.get_chi()

    def __repr__(self):
        dct = {'directions': self.directions, 'rudder_sets': self.rudder_sets}
        return '{}({})' % (self.__class__, dct)


class SpatialAgents(Agents):

    def __init__(self, directions, positions, rudder_sets, swimmers):
        super(SpatialAgents, self).__init__(directions, rudder_sets)
        self.positions = positions
        self.swimmers = swimmers

    def iterate(self, dt, obstructor):
        super(SpatialAgents, self).iterate(dt)
        self.positions, dr = self.swimmers.displace(self.positions, dt)
        obstructor.obstruct(self.positions, dr, self.directions)

    def __repr__(self):
        dct = {'directions': self.directions, 'positions': self.positions,
               'rudder_sets': self.rudder_sets, 'swimmers': self.swimmers}
        return '{}({})' % (self.__class__, dct)


def agents_factory(rng, dim, n, aligned_flag,
                   chi, onesided_flag,
                   p_0, tumble_chemo_flag,
                   Dr_0, rotation_chemo_flag):
    ds = directions.make_directions(n, dim, aligned_flag=aligned_flag, rng=rng)
    dc_dx_measurer = measurers.spatial_dc_dx_factory(ds)
    rudder_sets = rudders.rudder_set_factory(onesided_flag, chi,
                                             dc_dx_measurer, rng,
                                             tumble_chemo_flag, p_0,
                                             rotation_chemo_flag, Dr_0, dim)
    return Agents(ds, rudder_sets)


def spatial_agents_factory(rng, dim, n, aligned_flag,
                           v_0,
                           L, origin_flags, obstructor,
                           chi, onesided_flag,
                           p_0, tumble_chemo_flag,
                           Dr_0, rotation_chemo_flag,
                           spatial_chemo_flag, dt_mem, t_mem, time,
                           c_field=None):
    ds = directions.make_directions(n, dim, aligned_flag=aligned_flag, rng=rng)
    ps = positions.positions_factory(n, dim, L, origin_flags, rng, obstructor)
    dc_dx_measurer = measurers.dc_dx_factory(spatial_chemo_flag,
                                             ds,
                                             ps, v_0, dt_mem, t_mem, p_0, Dr_0,
                                             time,
                                             c_field)
    rudder_sets = rudders.rudder_set_factory(onesided_flag, chi,
                                             dc_dx_measurer, rng,
                                             tumble_chemo_flag, p_0,
                                             rotation_chemo_flag, Dr_0, dim)
    swims = swimmers.Swimmers(v_0, ds)
    return SpatialAgents(ds, ps, rudder_sets, swims)
