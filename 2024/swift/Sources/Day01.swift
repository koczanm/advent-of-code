import Algorithms

struct LocationList {
    var left: [Int]
    var right: [Int]
}

struct Day01: AdventDay {
    var data: String

    var locationList: LocationList {
        let pairs = data.split(separator: "\n").compactMap { line in
            let pair = line.split(separator: "   ").compactMap { Int($0) }
            return pair.count == 2 ? (pair[0], pair[1]) : nil
        }
        return pairs.reduce(into: LocationList(left: [], right: [])) { result, pair in
            result.left.append(pair.0)
            result.right.append(pair.1)
        }
    }

    func part1() -> Int {
        zip(locationList.left.sorted(), locationList.right.sorted())
            .map { abs($0 - $1) }
            .reduce(0, +)
    }

    func part2() -> Int {
        let counts = locationList.right.reduce(into: [:]) { counts, locationId in
            counts[locationId, default: 0] += 1
        }
        return locationList.left.reduce(0) { accumulator, locationId in
            accumulator + locationId * counts[locationId, default: 0]
        }
    }
}
