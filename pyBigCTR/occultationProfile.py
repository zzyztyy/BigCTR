from netCDF4 import Dataset
import os
import matplotlib.pyplot as plt


def get_lon_state(lon):
    if -120 < lon < -30:
        return 'American'
    elif -30 < lon < 60:
        return 'Africa'
    elif 60 < lon < 150:
        return 'Asia'
    else:
        return 'Pacific'


def chose_data(filename, count):
    f = Dataset(filename)
    botlct = f.botlct
    toplct = f.toplct
    botlon = f.botlon
    toplon = f.toplon
    year = f.year
    month = f.month
    day = f.day
    yymmdd = [str(year), str(month), str(day)]
    msl_alt = f.variables['MSL_alt'][:]
    geo_lat = f.variables['GEO_lat'][:]
    geo_lon = f.variables['GEO_lon'][:]
    elec_dens = f.variables['ELEC_dens'][:]

    if 17.5 < min(botlct, toplct) < 23.5 or 17.5 < max(botlct, toplct) < 23.5:
        if abs(botlon - toplon) < 180:
            # if botlon < -76.87 < toplon or botlon > -76.87 > toplon:
            if -180 < toplon < 180:
                print(count, botlct, toplct, botlon, toplon)
                print(filename)
                alt, lat, lon, den = [], [], [], []
                for i in range(len(geo_lon)):
                    if abs(geo_lat[i]) < 40:
                        alt.append(msl_alt[i])
                        lat.append(geo_lat[i])
                        den.append(elec_dens[i])
                        lon.append(geo_lon[i])
                if len(alt) > 0:
                    state = get_lon_state(toplon)
                    write_chosen_data(lat, lon, alt, den, yymmdd, botlct, toplct, state)
                return True
    return False


def write_chosen_data(lat, lon, alt, den, yymmdd, botlct, toplct, state):
    with open('D:/Program/BigCTR/Text/occPrf' + state + '.txt', 'a+') as f:
        # print('writing........................................')
        f.write('\n')
        f.write('/'.join(yymmdd) + ' lct ' + str([botlct, toplct]) + '\n')
        for i in range(len(lat)):
            s = ' '.join([str(x).rjust(10) for x in [lat[i], lon[i], alt[i], den[i]]]) + '\n'
            f.write(s)


def draw_chosen_data(lat, alt, den, filename, yymmdd):
    plt.scatter(lat, alt, s=2, c=den)
    # plt.show()
    plt.colorbar()
    plt.title(' '.join(yymmdd))
    plt.xlim([-40, 40])
    plt.ylim([0, 500])
    plt.savefig('D:/Program/BigCTR/Picture/occPrfJicamarca/' + filename[-40:] + '.png')
    plt.close()


def get_cdf_filename():
    count = 0
    path = 'D:/SpaceScienceData/champ2016_ionPrf/'
    dates = os.listdir(path)
    for date in dates:
        files = os.listdir(path + date)
        for file in files:
            filename = path + date + '/' + file
            if chose_data(filename, count):
                count += 1


if __name__ == '__main__':
    get_cdf_filename()
    # plt.colorbar()
    # plt.show()
