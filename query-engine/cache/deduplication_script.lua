local dataKey = KEYS[1]
local newValue = ARGV[1]
local newTimestamp = tonumber(ARGV[2])

local currentValue = redis.call('GET', dataKey)

if currentValue then
    local separatorIndex = string.find(currentValue, ':')
    if separatorIndex then
        local currentTimestamp = tonumber(string.sub(currentValue, 1, separatorIndex - 1))
        if currentTimestamp and currentTimestamp >= newTimestamp then
            return nil
        end
    end
end

redis.call('SET', dataKey, newValue)
return 1