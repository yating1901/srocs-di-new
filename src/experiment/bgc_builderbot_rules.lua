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
            type = 5
         },
      },
      target = {
         reference_index = vector3(0, 0, 0),
         offset_from_reference = vector3(1, 0, 0),
      },
   },
   {  safe_zone = 0.3,
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
         type = 3,
      },
   },
}
rules.customize_block_type = function(block)
      -- define type 5 as a block with a pink up face and an orange front face
      if block.tags.front ~= nil and block.tags.front.type == 1 then
         return 5
      end
      if block.tags.up ~= nil and block.tags.up.type == 2 then
         --if block.tags.front ~= nil and block.tags.front.type == 3 then
            return 6
         --end
      end
   end 
rules.selection_method = 'nearest_win'
return rules