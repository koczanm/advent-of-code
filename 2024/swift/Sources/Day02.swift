import Algorithms

enum Trend: Int {
    case decreasing = -1
    case increasing = 1
}

struct Report {
    let levels: [Int]

    var isSafe: Bool {
        guard levels.count > 1 else { return true }
        guard let trend = Trend(rawValue: (levels[0] - levels[1]).signum()) else { return false }

        return levels.adjacentPairs().allSatisfy { isDiffValid($0, $1, trend) }
    }

    var isSafeWithDampener: Bool {
        if isSafe {
            return true
        }

        let pairs = levels.adjacentPairs()

        var candidatesToRemove = Set<Int>()
        for (idx, (levelA, levelB)) in pairs.enumerated() where !isDiffValid(levelA, levelB, .decreasing) {
            candidatesToRemove.insert(idx)
            candidatesToRemove.insert(idx + 1)
            break
        }
        for (idx, (levelA, levelB)) in pairs.enumerated() where !isDiffValid(levelA, levelB, .increasing) {
            candidatesToRemove.insert(idx)
            candidatesToRemove.insert(idx + 1)
            break
        }

        for idx in candidatesToRemove {
            var levelsCopy = levels
            levelsCopy.remove(at: idx)
            let report = Report(levels: levelsCopy)
            if report.isSafe {
                return true
            }
        }

        return false
    }

    private func isDiffValid(_ levelA: Int, _ levelB: Int, _ trend: Trend) -> Bool {
        (levelA - levelB).signum() == trend.rawValue && (1 ... 3) ~= abs(levelA - levelB)
    }
}

struct Day02: AdventDay {
    var data: String

    var reports: [Report] {
        data.split(separator: "\n").compactMap { line in
            let levels = line.split(separator: " ").compactMap { Int($0) }
            return Report(levels: levels)
        }
    }

    func part1() -> Int {
        reports
            .filter { $0.isSafe }
            .count
    }

    func part2() -> Int {
        reports
            .filter { $0.isSafeWithDampener }
            .count
    }
}
