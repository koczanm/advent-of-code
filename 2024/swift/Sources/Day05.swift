struct Day05: AdventDay {
    var data: String

    var entities: ([Int: Set<Int>], [[Int]]) {
        let components = data.split(separator: "\n\n")
        guard components.count == 2 else { return ([:], []) }

        var rules: [Int: Set<Int>] = [:]
        for line in components[0].split(separator: "\n") {
            let parts = line.split(separator: "|")
            guard parts.count == 2,
                  let page = Int(parts[0]),
                  let furtherPage = Int(parts[1])
            else { continue }

            rules[page, default: Set<Int>()].insert(furtherPage)
        }

        let updates = components[1].split(separator: "\n").compactMap { line in
            line.split(separator: ",").compactMap { Int($0) }
        }
        return (rules, updates)
    }

    func areOrdered(_ pages: [Int], _ rules: [Int: Set<Int>]) -> Bool {
        var visitedPages = Set<Int>()
        var isOrdered = true
        for page in pages {
            if let furtherPages = rules[page], !furtherPages.isDisjoint(with: visitedPages) {
                isOrdered = false
                break
            }
            visitedPages.insert(page)
        }
        return isOrdered
    }

    func part1() -> Int {
        let (rules, updates) = entities
        return updates.filter { areOrdered($0, rules) }
            .compactMap { $0.middle }
            .reduce(0, +)
    }

    func part2() -> Int {
        let (rules, updates) = entities
        let sortPredicate: (Int, Int) -> Bool = { pageA, pageB in
            rules[pageA]?.contains(pageB) ?? false
        }
        return updates.filter { !areOrdered($0, rules) }
            .map { $0.sorted(by: sortPredicate) }
            .compactMap { $0.middle }
            .reduce(0, +)
    }
}

extension Array {
    var middle: Element? {
        guard count != 0 else { return nil }

        let middleIndex = (count > 1 ? count - 1 : count) / 2
        return self[middleIndex]
    }
}
