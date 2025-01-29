struct WordSearch {
    let grid: [[Character]]

    var height: Int {
        return grid.count
    }

    var width: Int {
        guard height > 0 else { return 0 }
        return grid[0].count
    }

    func countOccurances(of word: String) -> Int {
        var count = 0
        for (y, row) in grid.enumerated() {
            for x in row.indices {
                count += countOccurancesAt(x, y, of: word)
            }
        }
        return count
    }

    func countXOccurances(of word: String) -> Int {
        guard word.count % 2 == 1 else { return 0 }

        var count = 0
        for (y, row) in grid.enumerated() {
            for x in row.indices {
                count += countXOccurancesAt(x, y, of: word)
            }
        }
        return count
    }

    private func withinBounds(_ x: Int, _ y: Int) -> Bool {
        return 0 ..< width ~= x && 0 ..< height ~= y
    }

    private let directions: [(Int, Int)] = [
        (0, 1), // Right
        (0, -1), // Left
        (1, 0), // Down
        (-1, 0), // Up
        (1, 1), // Down-Right
        (1, -1), // Down-Left
        (-1, 1), // Up-Right
        (-1, -1), // Up-Left
    ]

    private func countOccurancesAt(_ x: Int, _ y: Int, of word: String) -> Int {
        var count = 0
        for (dx, dy) in directions {
            var matchCount = 0
            for step in 0 ..< word.count {
                let newX = x + dx * step
                let newY = y + dy * step

                guard withinBounds(newX, newY) else { break }

                if grid[newY][newX] == word[step] {
                    matchCount += 1
                } else {
                    break
                }
            }

            if matchCount == word.count {
                count += 1
            }
        }
        return count
    }

    private let xDirections: [(Int, Int)] = [
        (1, 1), // Down-Right
        (1, -1), // Down-Leff
    ]

    private func countXOccurancesAt(_ x: Int, _ y: Int, of word: String) -> Int {
        guard word.count % 2 == 1 else { return 0 }

        let wordHalf = word.count / 2

        if grid[y][x] != word[wordHalf] {
            return 0
        }

        var matchCount = 1
        for (dx, dy) in xDirections {
            for step in 1 ... wordHalf {
                let newX = x + dx * step
                let newY = y + dy * step
                let newXOpp = x - dx * step
                let newYOpp = y - dy * step

                guard withinBounds(newX, newY) && withinBounds(newXOpp, newYOpp) else { break }

                if grid[newY][newX] == word[wordHalf + step] && grid[newYOpp][newXOpp] == word[wordHalf - step] {
                    matchCount += 1
                } else if grid[newY][newX] == word[wordHalf - step] && grid[newYOpp][newXOpp] == word[wordHalf + step] {
                    matchCount += 1
                } else {
                    break
                }
            }
        }
        return matchCount == word.count ? 1 : 0
    }
}

struct Day04: AdventDay {
    var data: String

    var wordSearch: WordSearch {
        WordSearch(grid: data.split(separator: "\n").compactMap { Array($0) })
    }

    func part1() -> Int {
        wordSearch.countOccurances(of: "XMAS")
    }

    func part2() -> Int {
        wordSearch.countXOccurances(of: "MAS")
    }
}

extension StringProtocol {
    subscript(_ offset: Int) -> Character { self[index(startIndex, offsetBy: offset)] }
}
