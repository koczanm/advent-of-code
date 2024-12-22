import Algorithms

struct MulInstruction {
    let multiplicand: Int
    let multiplier: Int
    let enabled: Bool

    var product: Int {
        multiplicand * multiplier
    }
}

struct Day03: AdventDay {
    var data: String

    var instructions: [MulInstruction] {
        let pattern = /do(?:n't)?\(\)|mul\((\d+),(\d+)\)/
        let matches = data
            .split(separator: "\n")
            .compactMap { line in line.matches(of: pattern) }
            .reduce([], +)

        var enabled = true
        var instructions = [MulInstruction]()
        for match in matches {
            switch match.0 {
            case "do()":
                enabled = true
            case "don't()":
                enabled = false
            default:
                if let multiplicandString = match.1, let multiplerString = match.2 {
                    let multiplicand = Int(multiplicandString)!
                    let multipler = Int(multiplerString)!
                    instructions.append(
                        MulInstruction(multiplicand: multiplicand, multiplier: multipler, enabled: enabled)
                    )
                }
            }
        }
        return instructions
    }

    func part1() -> Int {
        instructions
            .map { $0.product }
            .reduce(0, +)
    }

    func part2() -> Int {
        return instructions
            .map { $0.enabled ? $0.product : 0 }
            .reduce(0, +)
    }
}
