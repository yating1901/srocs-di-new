local user_code = {}
require "bit32"
-- Set Face Color --
user_code.set_face_color = function(face, color)
   if face == "north" then
      robot.directional_leds.set_single_color(1, color)
      robot.directional_leds.set_single_color(2, color)
      robot.directional_leds.set_single_color(3, color)
      robot.directional_leds.set_single_color(4, color)
   elseif face == "east" then
      robot.directional_leds.set_single_color(5, color)
      robot.directional_leds.set_single_color(6, color)
      robot.directional_leds.set_single_color(7, color)
      robot.directional_leds.set_single_color(8, color)
   elseif face == "south" then
      robot.directional_leds.set_single_color(9, color)
      robot.directional_leds.set_single_color(10, color)
      robot.directional_leds.set_single_color(11, color)
      robot.directional_leds.set_single_color(12, color)
   elseif face == "west" then
      robot.directional_leds.set_single_color(13, color)
      robot.directional_leds.set_single_color(14, color)
      robot.directional_leds.set_single_color(15, color)
      robot.directional_leds.set_single_color(16, color)
   elseif face == "top" then
      robot.directional_leds.set_single_color(17, color)
      robot.directional_leds.set_single_color(18, color)
      robot.directional_leds.set_single_color(19, color)
      robot.directional_leds.set_single_color(20, color)
   elseif face == "bottom" then
      robot.directional_leds.set_single_color(21, color)
      robot.directional_leds.set_single_color(22, color)
      robot.directional_leds.set_single_color(23, color)
      robot.directional_leds.set_single_color(24, color)
   end
end

--define tree structure--
--user_code.tree={3,2,3,0,0,0}
--user_code.tree={3,2,1,2,0,2,4,2,0}
--user_code.tree={3,2,1,18,0,0,18,0,4,2,0}
--user_code.tree={3,3,1,18,0,0,2,0,18,0,0}
--user_code.tree={7,0,7,16,0,5,0,0,16,0,0}
--user_code.tree={23,0,0,7,16,0,21,0,0,0,16,0,0}
--user_code.tree={15,17,0,0,17,0,0,17,0,0,17,0,0}
user_code.tree={15,1,0,1,0,1,0,1,0}
--assign number to faces--
user_code.face_to_number = {
   north  = 1,
   east   = 2,
   south  = 3,
   west   = 4,
   top    = 5,
   bottom = 6,
}

user_code.num_to_face = {
   "north", "east", "south", "west", "top", "bottom"
}

user_code.face_to_order={}
--store directed faces--
user_code.order_to_face = {}
function user_code.set_directed_faces(identifier)
   -- assume the Top face is forever "top" --
   map={1, 2, 3, 4, 1, 2}  --surrounded face would be north,east,south,west
   face_number = user_code.face_to_number[identifier]
   
   user_code.order_to_face[4]   = identifier                                   --parent
   user_code.order_to_face[3]   = user_code.num_to_face[map[face_number + 1]]  --left
   user_code.order_to_face[2]   = user_code.num_to_face[map[face_number + 2]]  --front
   if face_number == 1 then
      user_code.order_to_face[1] = "west"   --parent face is north face, then right face is west face
   else
      user_code.order_to_face[1] = user_code.num_to_face[map[face_number - 1]]
   end
   user_code.order_to_face[5] = "top"
   user_code.order_to_face[6] = "bottom"

   for index = 1, 6 do 
      user_code.face_to_order[user_code.order_to_face[index]] = index
   end
end

--count the number of directly connected blocks
function user_code.count_children(internal_configuration)
   local num = 0
   local configuration = internal_configuration
   --print("configuration", configuration)
   if configuration ~= nil then
      for index = 1, 6 do
         if bit32.band(configuration, bit32.lshift(1, index-1)) ~= 0 then
            num = num +1
         end
      end 
   end
   --print("num", num)
   return num
end

-- Get one branch--
function user_code.get_one_branch(root_index, branch_data)
   local start_index 
   start_index = root_index    
   local final_index
   local tree_data
   tree_data = branch_data
   final_index = start_index + user_code.count_children(tree_data[start_index])

   while final_index ~= start_index do
      start_index = start_index + 1
      final_index = final_index + user_code.count_children(tree_data[start_index])
   end
   --print("final_index", final_index)
   return final_index
end

-- allocate branch data for its child faces--
user_code.tx_as_initiator = {}
function user_code.allocate_branch()
   local start_index = 1
   local order = {6,5,4,3,2,1}
   if #robot.branch_data > 0 then 
      for key, index in pairs(order) do
         if bit32.band(robot.branch_data[1], bit32.lshift(1, index-1)) ~= 0 then
            face_name = user_code.order_to_face[index]
            user_code.tx_as_initiator[face_name] = {}
            start_index = start_index + 1
            last_index = user_code.get_one_branch(start_index, robot.branch_data)
            if start_index <= #robot.branch_data then
               for branch_index = start_index, last_index do
                  table.insert(user_code.tx_as_initiator[face_name], robot.branch_data[branch_index])
               end
            end
            start_index = last_index 
            --light color
            if index ~= 5 then
               user_code.set_face_color(user_code.order_to_face[index],"magenta")
            else
               user_code.set_face_color(user_code.order_to_face[index],"orange")
            end
            --enable initiator
            for identifier, radio in pairs(robot.radios) do
               if identifier == user_code.order_to_face[index] then
                  radio.initiator_policy = "once"
               end
            end
         else
            user_code.set_face_color(user_code.order_to_face[index],"green")
         end
      end
   end
end

function user_code.my_tx_as_initiator(identifier)
   sub_branch = {}
   if user_code.tx_as_initiator[identifier] ~= nil then 

      sub_branch = user_code.tx_as_initiator[identifier]
   end
   return sub_branch
end


function user_code.my_rx_as_target(identifier, data)
   -- get branch data for its own --
   robot.branch_data = {}
   for msg_index, message in ipairs(data) do
      for byte_index, byte in ipairs(message) do
         --print(robot.id, msg_index, byte_index, byte)
         table.insert(robot.branch_data, byte)
      end
   end
end

--response messages table--
user_code.initiatoe_rx_table={}
function user_code.my_rx_as_initiator(identifier, data)
   user_code.initiatoe_rx_table[identifier] = {}
   if #data>0 then
      for msg_index, message in ipairs(data) do
         for byte_index, byte in ipairs(message) do 
            table.insert(user_code.initiatoe_rx_table[identifier], byte)
         end
      end
      robot.radios[identifier].haschild= true
   end
end

-- parent face response functor
function user_code.my_tx_as_target(identifier) 
   return user_code.tx_as_target
end

--get the info of which faces has a child
user_code.tx_as_target={}
function user_code.collect_messages()
   robot.childstate = 0
   for identifier, radio in pairs(robot.radios) do
      if radio.haschild == true  then
         robot.childstate = bit32.bor(robot.childstate, bit32.lshift(1, user_code.face_to_order[identifier]-1))
      end
   end
   user_code.tx_as_target={}
   --collect in the order: R,F,L,T,B
   for index=1, 6 do
      --if index ~= 4 then  --exlcude parent face
         face_name = user_code.order_to_face[index]
         if user_code.initiatoe_rx_table[face_name] ~= nil then
            for msg_index, msg in pairs(user_code.initiatoe_rx_table[face_name]) do
               table.insert(user_code.tx_as_target,msg)
            end
         end
      --end
   end
   table.insert(user_code.tx_as_target, robot.childstate)  --internal configuration
end

--cut relative branch in the robot.branch_data
user_code.drop_list = {}
function user_code.get_drop_list(bit_index)
   local list = {}
   local face_has_top_branch = bit_index

   face_to_be_cut = 3-face_has_top_branch
   table.insert(list, face_to_be_cut)    --index for branch to be cut
   if face_to_be_cut >=2 then
      table.insert(list, face_to_be_cut-2)
   else
      table.insert(list, face_to_be_cut+2)
   end
   user_code.drop_list = list
end


--clean face_index of drop_list in the robot.branch_data 
function user_code.clean_root_tree()
   local start_index = 1
   local end_index
   local new_branch_data = {}
   local change_index_list = {}
   --new_branch_data = robot.branch_data  !!!???
   for data_index, data in pairs(robot.branch_data) do 
      table.insert(new_branch_data, data)
   end
   for bit_index = 5, 0, -1 do
      if bit32.band(new_branch_data[1], bit32.lshift(1, bit_index)) ~= 0 then
         start_index = start_index+1
         end_index = user_code.get_one_branch(start_index, new_branch_data)
         for index, key in pairs(user_code.drop_list) do
            if key == bit_index then
               table.insert(change_index_list, start_index)
               print("change_index_list", start_index)                  
            end
         end
         start_index = end_index
      end
   end
   for new_index, new_data_index in pairs(change_index_list) do 
      new_branch_data[new_data_index]= bit32.band(new_branch_data[new_data_index],  
                                             bit32.bnot(bit32.lshift(1, user_code.face_to_order["top"]-1))) ---set 0
      --table.remove(new_branch_data, new_data_index+1)    --1 = 1+ user_code.get_one_branch(start_index+1+1) !!!  
      new_branch_data[new_data_index+1] = nil
   end 
   robot.branch_data = {}
   for new_index, new_data in pairs(new_branch_data) do 
      if new_data ~= nil then 
         table.insert(robot.branch_data, new_data)
         print("new_branch_data", new_index, new_data)
      end
   end
   robot.clean_tree = true 
end 


--Locate at the branch with a top child, 
function user_code.locate_branch()
   local start_ptr = 1
   local end_ptr
   local bit_index
   for bit_index = 5, 0, -1 do
      if bit32.band(user_code.structure_being_built[1], bit32.lshift(1, bit_index)) ~= 0 then
         start_ptr = start_ptr+1
         end_ptr = user_code.get_one_branch(start_ptr, user_code.structure_being_built)
         for child_index = start_ptr, end_ptr do 
            if bit32.band(user_code.structure_being_built[child_index], 			
                           bit32.lshift(1,user_code.face_to_order["top"]-1)) ~= 0 then
               user_code.get_drop_list(bit_index)
               robot.top_detected = true
            end   
         end
         start_ptr = end_ptr
      end
   end
end


--check if the structure has one top child
user_code.structure_being_built = {}
function user_code.get_structure_being_built()
   user_code.structure_being_built = {}
   for index = 1, #user_code.tx_as_target do
      table.insert(user_code.structure_being_built,user_code.tx_as_target[#user_code.tx_as_target+1-index])
   end
end

--
function user_code.insert_tree()
   local start_index = 1
   local end_index
   local inserted_list = {}
   local insert_data
   --record child position
   for bit_index = 5, 0, -1 do
      if bit32.band(robot.branch_data[1], bit32.lshift(1, bit_index)) ~= 0 then
         start_index = start_index+1
         end_index = user_code.get_one_branch(start_index, robot.branch_data)
         table.insert(inserted_list, start_index)
         start_index = end_index
      end
   end
   --set 1
   for index = 1, #inserted_list do 
      insert_index = inserted_list[index]
      robot.branch_data[insert_index] = bit32.bor(robot.branch_data[insert_index], 			
                                                   bit32.lshift(1,user_code.face_to_order["top"]-1))      --set 1
      table.insert(robot.branch_data, insert_index+1, 0)   --insert one isolated child
      for rest_data = index + 1, #inserted_list do
         inserted_list[rest_data] = inserted_list[rest_data] + 1  
      end
   end 
   robot.inserted_tree = true
end

-- init method --
function user_code.init()
   robot.isroot = false
   robot.blockstate = "Idle"
   robot.directional_leds.set_all_colors("black")
   robot.childstate = 0
   robot.branch_data = {} --should be an array
   robot.top_detected = false
   robot.clean_tree = false
   robot.inserted_tree = false
   -- define the root block
   if robot.id == "block0" then
      robot.isroot = true
      robot.radios["north"].parent = true
      robot.blockstate = "Query"
      user_code.set_directed_faces("north")
      robot.branch_data = user_code.tree
   end
	
   for id, radio in pairs(robot.radios) do
      radio.initiator_policy = "disable"
      radio.parent = false
      radio.haschild = false
      -- non-zero length payload shown in purple
      radio.tx_as_initiator = user_code.my_tx_as_initiator
      --radio.rx_as_initiator = function() end
      radio.rx_as_initiator = user_code.my_rx_as_initiator
      -- zero length payload shown in cyan
      --radio.tx_as_target = function() return {} end
      radio.tx_as_target = user_code.my_tx_as_target 
      radio.rx_as_target = user_code.my_rx_as_target
   end
end

-- step method --
function user_code.step(time)
  
   for identifier, radio in pairs(robot.radios) do
      if robot.blockstate == "Idle" then
         if radio.role == "target" and #radio.rx_data > 0 then
            if identifier == "bottom" or identifier == "up" then
               robot.blockstate = "Idle"
               radio.parent = false
               robot.directional_leds.set_all_colors("green")
	            user_code.tx_as_target={}
	            table.insert(user_code.tx_as_target, 0)
            else
               radio.parent = true
               robot.blockstate = "Query"
               robot.branch_data = radio.rx_data
               user_code.set_directed_faces(identifier)
               break --One block only have one parent face--
            end
         end    	
      else
         user_code.collect_messages()
         user_code.allocate_branch()
         --check if the structure is completed--
         length = #robot.branch_data
         if robot.isroot == true then
            --check if the first layer has been finished: #user_code.tx_as_target = 9 --
            if #user_code.tx_as_target == 9 and robot.inserted_tree == false then
               user_code.insert_tree()
            end
            --check if top child has been detected--
            if #user_code.tx_as_target > 9 then
               user_code.get_structure_being_built()
               user_code.locate_branch()    -- be careful if there are two top faces connected!
               if robot.top_detected == true and robot.clean_tree == false then
                  user_code.clean_root_tree()  --remove drop_list{}, child_face = top 
               end
            end
            if #user_code.tx_as_target == length then 
               iscompleted = true
               for index = 1, length  do
                  iscompleted =  iscompleted and (robot.branch_data[index] == user_code.tx_as_target[length + 1 - index])
               end
            end
            if iscompleted == true then
               robot.directional_leds.set_all_colors("blue")
            end
         end
      end

   end
end

-- reset method --
function user_code.reset()
   
end

return user_code


-- if time % 9 == 0 then
--    robot.directional_leds.set_single_color(21,"blue")
-- end
--robot.radios["east"].initiator_policy = "once"