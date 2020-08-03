-- just as a reminder {black = 0, pink = 1, orange = 2, green = 3, blue = 4}

local rules = {}
rules.list = {
   {
      rule_type = 'pickup',
      structure = {
         {
            index = vector3(0, 0, 0),
            type = 0
         }
      },
      target = {
         reference_index = vector3(0, 0, 0),
         offset_from_reference = vector3(0, 0, 0),
      },
   },
   {
      rule_type = 'place',
      structure = {
         {
            index = vector3(0, 0, 0),
            type = 6
         },
      },
      target = {
         reference_index = vector3(0, 0, 0),
         offset_from_reference = vector3(0, 0, 1),
      },
   },
}
rules.customize_block_type = function(block)
      if block.tags.up ~= nil and block.tags.up.type == 2 then
         return 6
      end
   end 
rules.selection_method = 'nearest_win'
return rules